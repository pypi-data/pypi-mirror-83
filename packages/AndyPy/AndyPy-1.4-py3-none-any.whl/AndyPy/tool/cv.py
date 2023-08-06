import cv2
from matplotlib import pyplot as plt
from math import ceil

__all__ = ["imshow","subplot"]

def imshow(img,title='',show=True,xyticks=(True,True)):
    '''显示图片 @param img obj of cv2.read(file).'''
    # 设置汉字不乱码
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 设置XY轴刻度显示与否
    if xyticks[0]: plt.xticks([])
    if xyticks[0]: plt.yticks([])
    plt.title(title)
    plt.imshow(img_rgb)
    if show: plt.show()
    
def subplot(imgs=[],M=0,titles=[],left=0, bottom=0, right=1, top=1,wspace=0, hspace=0.01):
    '''显示多张图片，M为显示图片的矩阵{eg:23 or [10,12] or (10,12)}'''
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1,wspace=0, hspace=0.01)
    # 设置矩阵行列数
    (nrows,ncols) = (M[0],M[1]) if(type(M) in [tuple,list]) else (M//10,M%10)
    if M==0: (nrows,ncols) = (ceil(len(imgs)**0.5),ceil(len(imgs)**0.5))
    # 设置显示多张子图
    for i,img in enumerate(imgs,start=1):
        plt.subplot(nrows,ncols,i)
        imshow(img,titles[i],show=False) if i<len(titles) else imshow(img,show=False)
    plt.show()