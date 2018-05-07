# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import requests


class LineWeatherNotify:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome("C:\ChromeDriver\chromedriver.exe", chrome_options=options)
        self.tenki = "http://www.jma.go.jp/jp/yoho/319.html"
        self.rosen = [
            ["都営新宿線", "https://transit.yahoo.co.jp/traininfo/detail/130/0/"],
            ["総武線快速", "https://transit.yahoo.co.jp/traininfo/detail/61/0/"],
            ["横須賀線", "https://transit.yahoo.co.jp/traininfo/detail/29/0/"]
        ]
        self.token = "Token"  # ここにトークンを記載

    def get_info(self, tenki_url, rosen_info):
        # 初期値セット
        if tenki_url is None:
            tenki_url = self.tenki
        if rosen_info is None:
            rosen_info = self.rosen

        # 気象情報
        self.driver.get(tenki_url)

        weather_v = ""
        temp_v = ""
        rain_v = ""
        try:
            forecast = self.driver.find_element_by_class_name("forecast")
            weather_v = forecast.find_elements_by_class_name("weather")[0]. \
                find_element_by_tag_name("img").get_property("title")
            temp_v = forecast.find_elements_by_class_name("temp")[0]. \
                find_element_by_class_name("max").text
            rain_v = forecast.find_elements_by_class_name("rain")[0].text
        except exceptions.NoSuchElementException:
            if weather_v == "" and temp_v == "":
                return "Weather Information Get Error. Check URL.", None, None, None, None

        # 運行情報
        t_info_v = []
        for trains in rosen_info:
            t_info_tmp = [trains[0]]
            self.driver.get(trains[1])
            try:
                train_info = self.driver.find_element_by_id("mdServiceStatus").find_element_by_tag_name("p").text
            except exceptions.NoSuchElementException:
                train_info = "情報を取得できませんでした"

            t_info_tmp.append(train_info)
            t_info_v.append(t_info_tmp)

        # self.line_notify(weather_v, rain_v, temp_v, t_info_v)

        return "ok", weather_v, rain_v, temp_v, t_info_v

    def line_notify(self, weather_v, rain_v, temp_v, t_info_v):
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": "Bearer " + self.token}

        body = '■本日の気象予報\n' + \
               '天気　　：' + weather_v + '\n' + \
               '最高気温：' + temp_v + '\n' + \
               '==降水確率==\n' + \
               rain_v + '\n\n' + \
               '■運行情報'

        for info in t_info_v:
            body = body + '\n' + info[0] + '：' + info[1]

        # print(message)

        payload = {"message": body}
        requests.post(url, headers=headers, params=payload)


if __name__ == '__main__':
    lwn = LineWeatherNotify()
    message, weather, rain, temp, t_info = lwn.get_info(None, None)

    print(message)
    print(weather)
    print(rain)
    print(temp)
    print(t_info)

    lwn.line_notify(weather, rain, temp, t_info)
