#!/usr/bin/env python3
import re
import time

LOG_FILE = '/var/log/cisco.log'

def tail_f(filename):
    """
    지정된 파일의 끝에서부터 새로운 내용이 추가될 때마다 한 줄씩 반환하는 generator 함수.
    """
    with open(filename, 'r') as f:
        # 파일의 끝으로 이동
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)  # 새로운 로그 대기
                continue
            yield line

def parse_log_line(line):
    """
    로그 라인을 파싱하여 (timestamp, host, message) 튜플을 반환합니다.
    예시 로그:
      May 24 14:55:32 logserver router1: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to administratively down
    """
    # 정규식 패턴: 월 일 시간, 호스트, 나머지 메시지
    pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(.*)$'
    match = re.match(pattern, line)
    if match:
        timestamp = match.group(1)
        host = match.group(2)
        message = match.group(3)
        return timestamp, host, message
    else:
        return None

def main():
    print(f"Monitoring log file: {LOG_FILE}")
    # tail_f 함수를 이용해 파일의 새로운 로그 라인을 지속적으로 읽어옵니다.
    for line in tail_f(LOG_FILE):
        parsed = parse_log_line(line)
        if parsed:
            timestamp, host, message = parsed
            # 파싱된 결과를 포맷에 맞춰 출력
            print(f"{timestamp} {host}: {message.strip()}")
        else:
            # 파싱에 실패한 경우 원문 그대로 출력
            print(line.strip())

if __name__ == '__main__':
    main()
