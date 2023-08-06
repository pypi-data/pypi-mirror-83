'''
* @Filename: pics2pdf.py   
* @Description: 合并图片生成PDF 
* @author: Andy 
* @date: ${2019.01.12} ${20:25}
* @version: V2.0  
'''
import glob
import fitz #pip install PyMuPDF
import os

def pics2pdf(picdir):
    doc = fitz.open()
    picdir = picdir + "/*"
    for img in sorted(glob.glob(picdir)):   # 读取图片，确保按文件名排序
        print(img)
        imgdoc = fitz.open(img)             # 打开图片
        pdfbytes = imgdoc.convertToPDF()    # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)               # 将当前页插入文档
    if os.path.exists("allimages.pdf"):
        os.remove("allimages.pdf")
    doc.save("allimages.pdf")               # 保存pdf文件
    doc.close()

if __name__ == '__main__':
    picdir = './pic2pdf'
    pics2pdf(picdir)
