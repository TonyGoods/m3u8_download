# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 21:03
# @Author  : Tony Goods
# @FileName: main.py
# @Software: PyCharm
import sys
import os
from urllib.request import urlopen


def main(url):
    path = url[:url.rfind('/') + 1]
    m3u8_list = str(urlopen(url).read(), encoding="utf-8")
    m3u8_list = m3u8_list.split('\n')
    total = (len(m3u8_list) - 6) / 2
    now = 1
    for m3u8 in m3u8_list:
        if m3u8.find('.ts') != -1:
            m3u8_path = path + m3u8
            m3u8_video = urlopen(m3u8_path).read()
            with open('temp\\' + m3u8, 'wb') as f:
                f.write(m3u8_video)
                f.flush()
                print('已完成：' + str(now / total) + "%")
                now += 1
    os.popen('copy /b temp/*.ts temp/new.mp4')
    os.popen('del temp\\*.ts')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('请加上m3u8视频的网址')
    else:
        main(sys.argv[1])
# python main.py https://iqiyi.com-l-iqiyi.com/20190404/22397_5d2018a7/1000k/hls/index.m3u8
