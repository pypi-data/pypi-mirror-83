import cv2
from matplotlib import pyplot as plt

def imshow(img,title='',show=True):
    '''显示图片 @param img obj of cv2.read(file).'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.imshow(img_rgb)
    if show: plt.show()
    
def subplot(M=11,imgs=[],titles=[]):
    '''显示多张图片，M为显示图片的矩阵'''
    for i,img in enumerate(imgs):
        plt.subplot(M*10+i+1)
        imshow(img,titles[i],show=False) if i<len(titles) else imshow(img,show=False)
    plt.show()