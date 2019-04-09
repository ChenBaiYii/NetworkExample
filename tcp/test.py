import sys
import time

sent = 0
byte_count = 1024

while sent < byte_count:
    sent += 1
    # print("\r %d bytes sent " % (sent,), end="")
    # print("\r %d bytes sent " % sent, end="")
    print(f"\r {sent} bytes sent", end="")
    time.sleep(0.3)
    sys.stdout.flush()

print("over")
