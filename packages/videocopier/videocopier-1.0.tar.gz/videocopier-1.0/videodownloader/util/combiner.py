# -*- coding: utf-8 -*-
from moviepy.editor import VideoFileClip, AudioFileClip
import os
'''
合成指定文件夹下的同名音频与视频
'''

def addAudio2Video(folder = './'):
    '''
            合成指定文件夹下的同名mp3音频和mp4视频
    '''
    file_list = os.listdir(folder)
    os.mkdir(os.path.join(folder, r'combined'))
    for file in file_list:
        if file.endswith(r'.mp4'):
            file_name = file.replace(r'.mp4','')
            if os.path.exists(os.path.join(folder,file_name+r'.mp3')):
                print('正在合成',file_name)
                video = VideoFileClip(os.path.join(folder,file))
                audio = AudioFileClip(os.path.join(folder,file_name+r'.mp3'))
                new_video = video.set_audio(audio)
                new_video.write_videofile(os.path.join(folder,r'combined',file))
                print(file_name,'合成完成')