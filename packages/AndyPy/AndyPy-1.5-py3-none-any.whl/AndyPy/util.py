# -*- coding: UTF-8 -*-
import os
import re
import urllib
import urllib.request

__all__ = ["getHTNLText","saveMp4","save_as_docx","save_as_txt"]

def getHTNLText(url = "http://www.***"):
    '''1.获取网页'''
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    try:
        r = requests.get(url=url, headers=headers)
        # If r.status_code not equal to 200, an exception is raised.
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "generating an exception!"

def saveMp4(path = "./", filename = "demo", mp4url = 'https://***.mp4'):
    """2.保存Mp4视频"""
    if not os.path.exists(path):
        os.makedirs(path)
    filename = r'%s//%s' % (path, filename)
    print('start download: "%s.mp4-->%s"' %(filename, mp4url) )
    urllib.request.urlretrieve(mp4url,"%s.mp4" %filename)  
    print('file "%s.mp4" done' % filename)
    
def save_as_docx(path, filename, content):
    '''3.保存内容为word'''
    if not os.path.exists(path):
        os.makedirs(path)
    file = r'%s/%s.txt' % (path, filename)
    file=docx.Document()
    file.add_paragraph(content)
    file.save("%s/%s.docx" % (path, filename))

def save_as_txt(path, filename, content):
    '''3.保存内容为txt'''
    if not os.path.exists(path):
        os.makedirs(path)
    file = r'%s/%s.txt' % (path, filename)
    with open(file, 'a+', encoding='utf-8') as f:
        f.write(str(content))
        
if __name__ == '__main__':
    filename = 'demo'
    mp4url="https://vdn1.vzuu.com/SD/bfe2aa5c-1ae7-11e9-b8d9-0a580a449bfe.mp4?disable_local_cache=1&bu=com&expiration=1552888973&auth_key=1552888973-0-0-8cd68f2a2be26c89856baba5bf5b6431&f=mp4&v=hw"
    saveMp4(filename = filename, mp4url = mp4url)
