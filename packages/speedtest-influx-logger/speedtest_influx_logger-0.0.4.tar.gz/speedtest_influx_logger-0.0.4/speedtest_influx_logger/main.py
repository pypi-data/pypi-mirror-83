# System Imports
from datetime import datetime
from distutils.util import strtobool
import os
import re
import requests
from requests.auth import HTTPBasicAuth
import time

# Framework / Library Imports
import schedule
import speedtest

# Application Imports

# Local Imports

APP_VERSION = "0.0.4"

NODE_NAME = os.environ.get("NODE_NAME", "unknown_node")

INFLUX_HOST = os.environ.get("INFLUX_HOST", None)
INFLUX_PORT = ":"+str(os.environ.get("INFLUX_PORT", None))
INFLUX_USER = os.environ.get("INFLUX_USER", None)
INFLUX_PASS = os.environ.get("INFLUX_PASS", None)
INFLUX_DB = os.environ.get("INFLUX_DB", None)
TEST_FREQUENCY = int(os.environ.get("TEST_FREQUENCY", 60))


def check_speed(speedtester):
    try:
        server = speedtester.get_best_server()
        # Returns JSON string of server, including ping as "latency"
        ping = server["latency"]

        # Returns float of download speed in bytes: 23858332.89967406
        download = "{:.2f}".format(speedtester.download()/1000000)

        # Returns float of upload speed in bytes: 6458335.637879163
        upload = "{:.2f}".format(speedtester.upload()/1000000)
        speed_data = {
            "measurement": "internet_speed",
            "tags": {
                "host": NODE_NAME,
                "client_version": APP_VERSION
            },
            "fields": {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }

        if None not in [INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PASS, INFLUX_DB]:
            payload = f"internet_speed,host={NODE_NAME},client_version={APP_VERSION} download={float(download)},upload={float(upload)},ping={float(ping)} {time.time_ns()}"
            res = requests.request(
                "POST",
                url=INFLUX_HOST+INFLUX_PORT+"/write?db="+INFLUX_DB,
                data=payload,
                auth=HTTPBasicAuth(INFLUX_USER, INFLUX_PASS)
            )
            print(res.status_code)
            print(res.text)

        print("{} - Speedtest complete: {}/{}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(download),
                str(upload)
            )
        )
    except Exception as e:
        print("There was a problem")
        print(str(e))


def main():

    if None in [INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PASS, INFLUX_DB]:
        for i in ["INFLUX_HOST", "INFLUX_PORT", "INFLUX_USER", "INFLUX_PASS", "INFLUX_DB"]:
            if eval(i) is None:
                print(f"{i} is not configured")
        print()
        print("Unable to send data to Influx as not configured")

    schedule.every(TEST_FREQUENCY).minutes.do(check_speed, speedtest.Speedtest())

    print(f"Starting Scheduler from '{NODE_NAME}' [v{APP_VERSION}]")
    print(f"Speedtest runs every {TEST_FREQUENCY} minutes")

    check_speed(speedtest.Speedtest())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()