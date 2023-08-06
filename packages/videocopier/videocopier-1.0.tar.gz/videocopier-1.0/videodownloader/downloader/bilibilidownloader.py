# -*- coding: utf-8 -*-
import requests
import re
import os

'''
B站视频下载模块
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
dl_headers = {
    'Referer': r'https://www.bilibili.com/video/BV1aV41127Ay',
    'User-Agent': user_agent
}

def getBVStr(url):
    '''
            解析url获取BV号
    '''
    if url.startswith(r"BV"):
        return url.split('?')[0]
    else:
        return url.split('?')[0].split(r'/video/')[-1]

def biliDownload(url):
    '''
                根据url或bv号下载视频
    '''
    if url.startswith(r"BV"):
        url = r'https://www.bilibili.com/video/' + url
    if url.startswith("www"):
        url = r'https://' + url
    bv = ''
    certainPart = False
    if not 'p=' in url:
        url = url.split('?')[0]
        bv = url.split(r'/video/')[-1]
    else:
        certainPart = True
        bv = url.split('?')[0].split(r'/video/')[-1]
    
    os.mkdir(os.path.join(export_folder, bv))
    
    part = 1
    while True:
        part_url = ''
        if certainPart and part == 1:
            part_url = url
        elif certainPart and part == 2:
            break
        else:
            part_url = url + r'?p=' + str(part)
        pageHTML = requests.get(part_url, headers=dl_headers).text
        
        videoScriptStr = ''
        try:
            videoScriptStr = re.findall(r'<script>window.__playinfo__=(.+?)</script>', pageHTML)[0]
        except:
            break
        videoScriptStr = videoScriptStr + r'</script>'
        audioScriptStr = re.findall(r'"audio":(.+?)</script>', videoScriptStr)[0]
        videoStr = re.findall(r'"baseUrl":"(.+?)"', videoScriptStr)[0]
        audioStr = re.findall(r'"baseUrl":"(.+?)"', audioScriptStr)[0]
        
        print('正在下载', bv, '的第', part, '个视频')
        save_video_name = bv + r'-Part' + str(part) + r'.mp4' if not certainPart else bv + r'.mp4'
        video = open(os.path.join(export_folder, bv, save_video_name), 'wb')
        res = requests.get(videoStr, headers=dl_headers)
        for block in res.iter_content(chunk_size=1024):
            video.write(block)
        video.close()
        print(bv, '的第', part, '个视频已下载完成')

        print('正在下载', bv, '的第', part, '个音频')
        save_audio_name = (bv + r'-Part' + str(part) + r'.mp3') if not certainPart else (bv + r'.mp3')
        audio = open(os.path.join(export_folder, bv, save_audio_name), 'wb')
        res = requests.get(audioStr, headers=dl_headers)
        for block in res.iter_content(chunk_size=1024):
            audio.write(block)
        audio.close()
        print(bv, '的第', part, '个音频已下载完成')
        part = part + 1
    
    if part == 2 and not certainPart:
        os.rename(os.path.join(export_folder, bv, bv + r'-Part1.mp4'), os.path.join(export_folder, bv, bv + r'.mp4'))
        os.rename(os.path.join(export_folder, bv, bv + r'-Part1.mp3'), os.path.join(export_folder, bv, bv + r'.mp3'))
        
    
if __name__ == '__main__':
    print(getBVStr('BV1Ct411H7rm?p=23'))
