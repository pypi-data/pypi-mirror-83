from distutils.core import setup

setup(
    name = 'videocopier',
    version = '1.0',
    description = 'bilibili视频下载工具',
    author = 'LJJ',
    author_email = 'mu_zi_liu_ri@163.com',
    py_modules = ['videodownloader.downloader.bilibilidownloader','videodownloader.util.combiner']
)