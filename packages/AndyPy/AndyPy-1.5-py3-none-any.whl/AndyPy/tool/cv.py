import cv2
from matplotlib import pyplot as plt
from math import ceil


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
    
def getGrayImg(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def getBinaryImg(grayImg):
    return cv.adaptiveThreshold(grayImg, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    
def getContours(binaryImg):
    contours,_ = cv.findContours(binaryImg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours
    
def getRectangles(contours):
    return [cv.boundingRect(cnt) for cnt in contours]
    
def sortByYX(roisxywh):
    roisxywh.sort(key=lambda l:(l[1],l[0]))
    prex,prey,_,_ = roisxywh[0]
    steps = []
    for i,(x, y, iw, ih) in enumerate(roisxywh):
        if(y-prey>20):
            steps.append(i)
        prey = y
    steps.insert(0,0)
    steps.append(len(roisxywh))
    steps.sort(reverse=True)
    i = steps.pop()
    while len(steps)!=0:
        j = steps.pop()
        tmp = roisxywh[i:j]
        ys = [x[1] for x in tmp]
        y_min = min(ys)
        for t in tmp:
            t[3] = t[3]+(t[1]-y_min)
            t[1]=y_min
        i = j
    roisxywh.sort(key=lambda l:(l[1],l[0]))
    
def cvDraw(img,recs_xywh=None,contours=None,recShow=True,recIndexShow=True):
    img_t = img.copy()
    if recs_xywh:
        for i,(x, y, iw, ih) in enumerate(recs_xywh):
            if recShow: cv.rectangle(img_t,(x, y),(x+iw, y+ih),(0,255,0),1)
            if recIndexShow: cv.putText(img_t, str(i), (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, 8)
    if contours:
        for i in range(len(contours)):
            cv.drawContours(img_t,contours,i,(0,0,255))
    imshow(img_t)
    
