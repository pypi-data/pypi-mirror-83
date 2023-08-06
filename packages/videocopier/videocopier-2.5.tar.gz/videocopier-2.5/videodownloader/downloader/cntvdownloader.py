# -*- coding: utf-8 -*-
import requests
import re
import os

'''
cntv视频下载模块

@author: LJJ
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
dl_headers = {
    'Referer': r'https://tv.cctv.com/',
    'User-Agent': user_agent
}


def getVideoCode(url):
    '''
            获得视频编号
    '''
    html = requests.get(url,headers=dl_headers).text
    video_code = re.findall(r'videoCenterId: "(.+?)"', html)[0]
    return str(video_code)



def cntvDownload(url):
    '''
                下载视频
    '''
    video_code = getVideoCode(url)
    video_file = open(os.path.join(export_folder,video_code + r'.mp4'),'wb')
    definations = [(8000,'1080P'),(4000,'720P'),(2000,'超清'),(1200,'高清'),(850,'标清'),(450,'流畅')]
    prifix = r'https://hls.cntv.lxdns.com/asp/hls/'
    middle = r'/0303000a/3/default/'
    suffix = r'.ts'
    maxDefination = ''
    for defination,description in definations:
        tempUrl = prifix + str(defination) + middle + video_code + r'/0.ts'
        status = requests.get(tempUrl,headers=dl_headers).status_code
        if status == 200:
            maxDefination = str(defination)
            print(video_code,'的最大清晰度为：',description)
            break
    
    segment = 0
    print("开始下载")
    while True:
        tempUrl = prifix + maxDefination + middle + video_code + r'/' + str(segment) + suffix
        res = requests.get(tempUrl,stream=True,headers=dl_headers)
        status = res.status_code
        if status == 200:
            for block in res.iter_content(chunk_size=1024):
                video_file.write(block)
            segment = segment + 1
        else:
            print('下载完成')
            video_file.close()
            break
    

    
if __name__ == '__main__':
    url=r'https://tv.cctv.com/2020/08/29/VIDEInZuloVLxh4eSVGy4Znh200829.shtml?spm=C55899450127.PGm7WxgwlTKs.0.0'
    cntvDownload(url)
    


