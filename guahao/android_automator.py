import sys
import os
import re
import time
import uiautomator2 as u2

def init(d):
    session = d.app_start('com.greenline.guahao', '.home.HomeActivity')
    d(resourceId="com.greenline.guahao:id/afa").set_text(" ")
    d(resourceId="com.greenline.guahao:id/fi1").set_text("陈震")
    d.send_action("search")
    d(resourceId="com.greenline.guahao:id/exl").child(textContains="复旦大学附属肿瘤医院徐汇院区").click()
    d(textContains="预约挂号").click()
    d(textContains="显示全部排班").click()

def search_shifts(d, date_str):
    while True:
        d(text="可预约").click()
        items = d(className="android.widget.ScrollView") \
            .child(className="android.view.ViewGroup") \
            .child()

        for i in range(len(items)):
            item = items[i]
            text = item.get_text()
            if date_str in text:
                status = items[i+7].get_text()
                if status == "预约":
                    item.click()
        print("============ checking ============")
        time.sleep(300)

if __name__ == '__main__':
    d = u2.connect('e7b4cc94')
    #init(d)
    date_str = "2021-08-02"
    search_shifts(d, date_str)
