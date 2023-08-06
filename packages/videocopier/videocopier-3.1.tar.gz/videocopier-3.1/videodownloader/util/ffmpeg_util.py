# -*- coding: utf-8 -*-
import os
from ffmpy import FFmpeg

'''
使用ffmpeg进行音视频操作

@author: MT
'''



def mergeP4P3(path):
    '''
            合成指定文件夹下的同名mp3音频和mp4视频
            path为单个视频文件夹的路径 如D:\PROJECT\scrapy\video-capture-tool\videodownloader\downloader\BV1254y1q7xy
    '''
    file_list = os.listdir(path)
    for file in file_list:
        if file.endswith(r'.mp4'):
            o_name,_ = os.path.splitext(file)
            if os.path.exists(os.path.join(path,o_name+r'.mp3')):
                print('正在合成',o_name)
                p4n = os.path.join(path, o_name + '.mp4')
                p3n = os.path.join(path, o_name + '.mp3')
                nname = os.path.join(path, o_name + '_finish.mp4')
                ff = FFmpeg(
                    inputs={p4n: None, p3n: None},
                    outputs={nname: '-c:v copy -c:a copy'}
                )
                try:
                    ff.cmd
                    ff.run()
                    os.remove(p4n)
                    os.remove(p3n)
                    os.renames(os.path.join(path, o_name + '_finish.mp4'),os.path.join(path, o_name + '.mp4'))
                    print(o_name, "合成完毕")
                except Exception as e:
                    raise e




if __name__ == '__main__':
    path = r'C:\coding\VideoCopier\videocopier\src\video-capture-tool\videodownloader\downloader\BV1254y1q7xy'
    mergeP4P3(path)












