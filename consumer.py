#!/usr/bin/env python3
import pika

# RabbitMQ 서버 주소 (중앙 로그 서버에 설치되어 있거나 네트워크 상 접근 가능)
rabbitmq_host = '192.168.1.101'  # 로그 서버의 IP 또는 도메인
rabbitmq_queue = 'syslog_logs'

def callback(ch, method, properties, body):
    log_message = body.decode('utf-8')
    print(f"수신된 로그: {log_message}")
    # 여기에 데이터베이스 저장, 리포트 생성, 알림 등 추가 후속 처리를 구현할 수 있습니다.

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)
    print("RabbitMQ 큐에서 메시지 소비 시작. 대기 중...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("종료합니다.")
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()
