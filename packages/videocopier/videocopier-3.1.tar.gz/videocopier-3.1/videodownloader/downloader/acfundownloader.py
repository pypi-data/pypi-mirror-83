# -*- coding: utf-8 -*-
import requests
import re
import os
import json
'''
acfun视频下载模块

@author: LJJ
'''

export_folder = r'./'
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
dl_headers = {
    'User-Agent': user_agent
}


def getVideoCode(url):
    '''
            解析url获取视频编号，作为文件夹名
    '''
    if url.startswith(r"ac"):
        return url.split('_')[0]
    else:
        return url.split('_')[0].split(r'/')[-1]



def acfunDownload(url):
    '''
                下载视频
    '''
    if url.startswith(r"ac"):
        url = r'https://www.acfun.cn/v/' + url
    if url.startswith(r"www"):
        url = r'https://' + url
    ac = getVideoCode(url)
    url = url.split('?')[0]
    certainPart = False
    if '_' in url:
        certainPart = True
    os.mkdir(os.path.join(export_folder, ac))
    
    part = 1
    html = requests.get(url,headers=dl_headers).text
    if not r'</li>' in html:
        certainPart = True
    else:
        part = len(re.findall(r'</li>', html))
    if certainPart:
        part = 1
    
    print('此视频共有',part,'P')
    tempPart = 1
    while tempPart <= part:
        tempPageUrl = ''
        if certainPart:
            tempPageUrl = url
        else:
            tempPageUrl = url + r'_' + str(tempPart)
        tempHTML = requests.get(tempPageUrl,headers=dl_headers).text
        tempHTML = re.sub(r'\\"',r'"',tempHTML)
        backupUrl = re.findall(r'"backupUrl":(.+?)]', tempHTML)[0] + r']'
        m3u8Url = json.loads(backupUrl)[0]
        m3u8File = open(os.path.join(export_folder,ac,str(tempPart) + '.m3u8'),'wb')
        res = requests.get(m3u8Url,stream=True,headers=dl_headers)
        for block in res.iter_content(chunk_size=1024):
            m3u8File.write(block)
        m3u8File.close()
        tsList = []
        m3u8File = open(os.path.join(export_folder,ac,str(tempPart) + '.m3u8'),'r')
        while True:
            line = m3u8File.readline()
            if r'.ts' in line:
                tsList.append(re.sub('\s','',line))
            if not line:
                break
        m3u8File.close()
        print('正在下载第',tempPart,'个视频')
        videoFile = open(os.path.join(export_folder,ac,ac + ('' if certainPart else '_' + str(tempPart)) + '.mp4'),'wb')
        for tsUrl in tsList:
            prifix = r'https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/hls/'
            res = requests.get(prifix + tsUrl,stream=True,headers=dl_headers)
            for block in res.iter_content(chunk_size=1024):
                videoFile.write(block)
        videoFile.close()
        tempPart = tempPart + 1
    print('全部下载完成')
    files = os.listdir(os.path.join(export_folder,ac))
    for file in files:
        if file.endswith(r'.m3u8'):
            os.remove(os.path.join(export_folder,ac,file))


if __name__ == '__main__':
    url=r'ac3202810'
    acfunDownload(url)
    


