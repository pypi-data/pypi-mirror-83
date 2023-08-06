# -*- coding: utf-8 -*-
import requests
import re
import os

'''
B站视频下载模块

@author: LJJ
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
cookie = r"LIVE_BUVID=AUTO3115713170022340; stardustvideo=1; rpdid=|(u|kk)J|m))0J'ul~uJu~|Yk; sid=89160sq9; im_notify_type_13878796=0; LIVE_PLAYER_TYPE=1; buvid3=F064F543-B276-4DF9-8E06-17DE02A3CEDD155832infoc; blackside_state=1; dy_spec_agreed=1; CURRENT_FNVAL=80; _uuid=612E4207-FE02-8D41-220B-20911597179B18512infoc; bp_video_offset_13878796=449935491123664012; PVID=8; finger=158939783; DedeUserID=4661578; DedeUserID__ckMd5=ec615f9d7d365898; SESSDATA=37e75701%2C1619331024%2C2196a*a1; bili_jct=e998f74ae827f1bda15dd43b0ebc5efd; CURRENT_QUALITY=120"
dl_headers = {
    'Referer': r'https://tv.cctv.com/',
    'User-Agent': user_agent,
    'cookie': cookie
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
    video_file = open(os.path.join(export_folder,video_code + r'.ts'),'wb')
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
    while True:
        tempUrl = prifix + maxDefination + middle + video_code + r'/' + str(segment) + suffix
        res = requests.get(tempUrl,stream=True,headers=dl_headers)
        status = res.status_code
        print("开始下载")
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
    


