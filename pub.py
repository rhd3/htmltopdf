#!/usr/bin/env python3
import socketserver
import re
import time
import pika

# RabbitMQ 설정 (RabbitMQ 서버가 중앙 로그 서버 내에 있거나 네트워크상에서 접근 가능)
rabbitmq_host = 'localhost'   # 또는 RabbitMQ 서버의 IP 주소
rabbitmq_queue = 'syslog_logs'
rabbit_conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = rabbit_conn.channel()
channel.queue_declare(queue=rabbitmq_queue)

def parse_syslog(message):
    try:
        decoded = message.decode('utf-8', errors='ignore')
    except Exception:
        decoded = str(message)
    # Cisco 로그 형식 예시: <PRI>Month Day HH:MM:SS device message
    pattern = r'<(\d+)>(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(.*)'
    match = re.match(pattern, decoded)
    if match:
        pri = int(match.group(1))
        timestamp = match.group(2)
        device = match.group(3)
        msg = match.group(4)
        # 간단하게 우선순위를 이용한 심각도 결정 (예시)
        severity = "INFO"  # 기본값, 실제로는 pri값을 기준으로 결정
        return f"{timestamp} {device} {severity}: {msg}"
    else:
        return f"{time.strftime('%b %d %H:%M:%S')} unknown INFO: {decoded}"

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        log_entry = parse_syslog(data)
        # RabbitMQ 큐에 로그 메시지 발행
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=log_entry)
        print(f"발행된 로그: {log_entry}")

if __name__ == "__main__":
    UDP_IP = "0.0.0.0"
    UDP_PORT = 514
    server = socketserver.UDPServer((UDP_IP, UDP_PORT), SyslogUDPHandler)
    print(f"Syslog 서버가 {UDP_IP}:{UDP_PORT}에서 대기 중...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("종료합니다.")
        server.shutdown()
        rabbit_conn.close()
