from urllib.parse import urlparse, parse_qs
import time
import re
import sys
import json
import requests
import subprocess
from playaudio import playaudio


def extract_expert_info(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    expert_id = path.split("/")[-1]
    kv = parse_qs(parsed_url.query)
    hosp_id = kv["hospitalId"][0]
    hosp_dept_id = kv["hospDeptId"][0]

    return [expert_id, hosp_dept_id, hosp_id]


def curl_check():
    output = subprocess.check_output("bash run.sh", shell=True)
    data = json.loads(output.decode("utf-8"))
    items = data["items"]
    shifts = []
    for item in items:
        shifts.extend(item["shiftCases"])
    for shift in shifts:
        d = shift["shiftDateFormat"]
        p = shift["price"] / 100
        s = shift["extraStateDesc"]
        print("{} - {}元 {}".format(d, p, s))
        if s != "约满":
            playaudio("alert.m4a")


if __name__ == "__main__":
    while True:
        result = curl_check()
        time.sleep(120)
