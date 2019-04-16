# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 21:03
# @Author  : Tony Goods
# @FileName: main.py
# @Software: PyCharm
import sys
import os
import threading
from urllib.request import urlopen

m3u8_list = []
path = ''
total = 0
now = 0
lock = threading.Lock()
locks = [True, True, True, True, True]


def download_thread(index):
    global path
    global m3u8_list
    global lock
    global now
    global locks

    m3u8s = m3u8_list[5 + index * 2:-2:10]
    for m3u8 in m3u8s:
        m3u8_path = path + m3u8
        while True:
            try:
                m3u8_video = urlopen(m3u8_path).read()
                with open('temp\\' + m3u8, 'wb') as f:
                    f.write(m3u8_video)
                    f.flush()
                    with lock:
                        now += 1
                        print('已完成：' + str(now / total * 100) + "%")
                break
            except:
                print('network is wrong.')
                pass
    locks[index] = False


def main(url, new_file_name):
    global total
    global locks
    global path
    global m3u8_list

    path = url[:url.rfind('/') + 1]
    m3u8_list = str(urlopen(url).read(), encoding="utf-8")
    m3u8_list = m3u8_list.split('\n')
    total = (len(m3u8_list) - 6) / 2

    threading.Thread(target=download_thread, args=(0,)).start()
    threading.Thread(target=download_thread, args=(1,)).start()
    threading.Thread(target=download_thread, args=(2,)).start()
    threading.Thread(target=download_thread, args=(3,)).start()
    threading.Thread(target=download_thread, args=(4,)).start()

    while locks[0] or locks[1] or locks[2] or locks[3] or locks[4]:
        continue
    os.system('copy /b temp\\*.ts temp\\' + new_file_name + '.mp4')
    os.popen('del temp\\*.ts')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('请加上m3u8视频的网址')
    else:
        main(sys.argv[1], sys.argv[2])
