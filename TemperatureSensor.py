from datetime import datetime
import time, os, glob, random

# Temperature code here

delay = 10  # (1800 for 30 minutes) (3600 for 1 hour)

while True:
    now = datetime.now()
    testTempF = random.randint(0,80)
    testTempC = int((testTempF - 32) * (5/9))

    # dd/mm/YY H:M:S
    chrono_str = now.strftime("%d/%m/%Y %H:%M:%S")
    out = f'{chrono_str} -> {testTempF}, {testTempC} (F, C)'
    print(out)
    with open("log.txt", "a") as log:
        toLog = f'{out}\n'
        log.write(toLog)
    time.sleep(delay)
