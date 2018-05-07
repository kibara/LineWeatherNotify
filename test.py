# -*- coding: utf-8 -*-

import unittest
from Main import LineWeatherNotify


class TestMain(unittest.TestCase):
    def test_get_info_ok(self):
        print("\n\n== Call test_get_info_ok ==")

        tenki = "http://www.jma.go.jp/jp/yoho/319.html"
        rosen = [
            ["都営新宿線", "https://transit.yahoo.co.jp/traininfo/detail/130/0/"],
            ["総武線快速", "https://transit.yahoo.co.jp/traininfo/detail/61/0/"],
            ["横須賀線", "https://transit.yahoo.co.jp/traininfo/detail/29/0/"]
        ]

        self.lwn = LineWeatherNotify()
        message, weather, rain, temp, t_info = self.lwn.get_info(tenki, rosen)
        self.assertEqual(message, 'ok')

        print(message)
        print(weather)
        print(rain)
        print(temp)
        print(t_info)

    def test_get_info_tenki_ng(self):
        print("\n\n== Call test_get_info_tenki_ng ==")
        # tenki = "http://www.jma.go.jp/jp/yoho/319.html"
        tenki = "http://www.jma.go.jp/jp/yoh/319.html"
        rosen = [
            ["都営新宿線", "https://transit.yahoo.co.jp/traininfo/detail/130/0/"],
            ["総武線快速", "https://transit.yahoo.co.jp/traininfo/detail/61/0/"],
            ["横須賀線", "https://transit.yahoo.co.jp/traininfo/detail/29/0/"]
        ]

        self.lwn = LineWeatherNotify()
        message, weather, rain, temp, t_info = self.lwn.get_info(tenki, rosen)
        self.assertEqual(message, 'Weather Information Get Error. Check URL.')

        print(message)
        print(weather)
        print(rain)
        print(temp)
        print(t_info)

    def test_get_info_rosen_ng(self):
        print("\n\n== Call test_get_info_rosen_ng ==")

        tenki = "http://www.jma.go.jp/jp/yoho/319.html"
        rosen = [
            ["都営新宿線", "https://transit.yahoo.co.jp/traininfo/detail/130/0/"],
            # ["総武線快速", "https://transit.yahoo.co.jp/traininfo/detail/61/0/"],
            ["総武線快速", "https://transit.yahoo.co.jp/traininf/detail/61/0/"],
            ["横須賀線", "https://transit.yahoo.co.jp/traininfo/detail/29/0/"]
        ]

        self.lwn = LineWeatherNotify()
        message, weather, rain, temp, t_info = self.lwn.get_info(tenki, rosen)
        self.assertEqual(t_info[1][1], '情報を取得できませんでした')

        print(message)
        print(weather)
        print(rain)
        print(temp)
        print(t_info)
