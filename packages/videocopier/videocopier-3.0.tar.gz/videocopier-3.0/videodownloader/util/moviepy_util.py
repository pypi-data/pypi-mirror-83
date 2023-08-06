# -*- coding: utf-8 -*-
from moviepy.editor import VideoFileClip, AudioFileClip
import os
'''
使用moviepy进行音视频操作

@author: LJJ
'''

def mergeP4P3(path):
    '''
            合成指定文件夹下的同名mp3音频和mp4视频
    '''
    file_list = os.listdir(path)
    for file in file_list:
        if file.endswith(r'.mp4'):
            file_name = file.replace(r'.mp4','')
            if os.path.exists(os.path.join(path,file_name+r'.mp3')):
                print('正在合成',file_name)
                video = VideoFileClip(os.path.join(path,file))
                audio = AudioFileClip(os.path.join(path,file_name+r'.mp3'))
                new_video = video.set_audio(audio)
                new_video.write_videofile(os.path.join(path,r'copy'+file))
                os.remove(os.path.join(path,file))
                os.remove(os.path.join(path,file_name+r'.mp3'))
                os.rename(os.path.join(path,r'copy'+file),os.path.join(path,file))
                print(file_name,'合成完成')
           
    
    
if __name__ == '__main__':
    path = r'C:\coding\VideoCopier\videocopier\src\video-capture-tool\videodownloader\downloader\d906b02539d741ca9fc42dfe2f0e986a'
