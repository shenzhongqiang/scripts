import time
import re
import sys
import json
import requests

SHIFT_URL = "https://www.guahao.com/expert/new/shiftcase?expertId={}&hospDeptId={}&hospId={}"
BASE_URL = "https://www.guahao.com"
headers = {
    "Cookie": "_sid_=16210853153490166676160028; _e_m=1621085315359; Hm_lvt_3a79c3f192d291eafbe9735053af3f82=1621085318; _ipgeo=province%3A%E4%B8%8A%E6%B5%B7%7Ccity%3A; searchHistory=%E9%99%88%E9%9C%87%2C%7C%2Cclear; JSESSIONID=node01lj9hlmvqfwn61gqd46watpafl294.node0; __wyt__=!PPKDN3fl2Z5RI4Y_21WuX0ni0GliN1lGP5J1-jd9QlJppucu-yqRW1k6gKWV1mxkJ7Vnje_mlGtSiwMNzqqEwlCHVOX5YTewjgr2HG1PbcKkhAUenyfGI7NYlpSEppcgL_1AzqynZ80Kltmpr1hY-xerbi6f49WTUpDwuhDqdxeFg; _fmdata=MPqlI8lWO6cpm95ca5IIQieiVaYmulica1V%2B5mXS1W7Ze1sp6Xwsjd7ASC5NHnmuJGFklzffLY%2FKd9SB8ll1%2BMcVMnh0AbA%2BvRWog8aO%2F9k%3D; _fm_code=eyJ2IjoiL01SWGxaaG5ibWdwcGVqR1IyWThGajJNV29oT01wand1Qkt4YytJSEs3TmQ0RkFkSnFJRGJLYURPY1hPQTRQaSIsIm9zIjoid2ViIiwiaXQiOjg2OSwidCI6ImxZd1Z0MGl4aEdVNEJUOFNwUzE2Q3dRK3Vqb0FpYjZFajJHejMwaVZzSWM4bGQ0T1dKTnp5NUJTdjJvdDlWSnUvZXVTM3lhN0ZNUHFFbnNjb0J6VHpRPT0ifQ%3D%3D; __rf__=Bez9vSBgRrkHqp3ic6xiuFJmD67/BqHTmnYm0uBYc07GU0Ohq5d+4rOpJqftwAASah1ESWD4GdP3CLAJVR5xDHcZwNX2fEbTLBFU+v1owcL/zWa8V66XMEoQeAgvreBo; _sh_ssid_=1621131752043; Hm_lpvt_3a79c3f192d291eafbe9735053af3f82=1621131755",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

def extract_expert_info(url):
    matched = re.search(r'guahao.com/expert/(.*)\?hospDeptId=(.*)&hospitalId=(.*)', url)
    if not matched:
        raise Exception("cannot extract expert info from URL: {}".format(url))
    expert_id = matched.group(1)
    hosp_dept_id = matched.group(2)
    hosp_id = matched.group(3)
    return [expert_id, hosp_dept_id, hosp_id]

def check(expert_id, hosp_dept_id, hosp_id):
    url = SHIFT_URL.format(expert_id, hosp_dept_id, hosp_id)
    r = requests.get(url, headers=headers, verify=False)
    content = r.content.decode("utf-8")
    data = json.loads(content)
    if data["hasError"]:
        raise Exception("failed to check shift status")
    shifts = data.get("data", {}).get("shiftSchedule", [])
    result = []
    for shift in shifts:
        shift_type = shift.get("type", -1)
        shift_clinictype = shift.get("clinicType", "")
        price = shift.get("price", 0.0)
        shift_date = shift.get("date")
        shift_url = shift.get("url", "")
        status = shift.get("status", -1)
        if shift_type == 2 or shift_clinictype == "专家" or price < 100:
            if status == 4:
                result.append({
                    "date": shift_date,
                    "url": BASE_URL + shift_url,
                })
    return result

if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print("Usage: {} <url>".format(sys.argv[0]))
    #    sys.exit(1)
    #url = sys.argv[1]
    url = "https://www.guahao.com/expert/125749779229250000?hospDeptId=131815041410686000&hospitalId=125358368239002000"
    expert_info = extract_expert_info(url)
    while True:
        result = check(*expert_info)
        print(result)
        time.sleep(300)
