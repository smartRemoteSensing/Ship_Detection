import os
from PIL import Image
import numpy as np
import cv2
import gdal
# 获取文件名绝对路径===========================
def getfilename(path):
    pathdir = os.listdir(path)  # 文件名保存为列表
    # print(pathdir)
    newdir = list(pathdir)  # 为了不改变原始列表

    j = 0
    for i in pathdir:
        newdir[j] = i.replace('HV', '')
        j += 1

    dir = pathdir  # dir保存完整文件名路径
    j = 0  # 文件计数
    for mname, filename in zip(pathdir, newdir):
        dir[j] = path + '\\' + mname + '\\' + filename + '.tiff'
        j = j + 1
    return dir,j  #返回绝对路径文件名 和文件个数
# 获取文件名绝对路径=========================
# #把0值当最小值把 ，均值+4倍标准差当做最大值进行拉伸

def minmaximg(width,heigh,img):
    bandMean = img.mean() #求波段均值
    bandStd = img.std() #求波段标准差
    min = img.min()
    max = bandMean + 4*bandStd  # 均值+4倍标准差最为最大值
    return min,max
##把0值当最小值把 ，均值 + 4倍标准差当做最大值进行拉伸
# 拉伸========================
def linearstretching(img,min,max):

    img=np.where(img > min, img, min)
    img=np.where(img < max, img, max)
    img = (img - min) / (max - min) * 255
    return img
# 拉伸========================
#读取图像
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
        return
    im_width = dataset.RasterXSize #栅格矩阵的列数
    im_height = dataset.RasterYSize #栅格矩阵的行数
    im_bands = dataset.RasterCount #波段数
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)#获取数据

    im_geotrans = dataset.GetGeoTransform()#获取仿射矩阵信息
    im_proj = dataset.GetProjection()#获取投影信息
    HH_band = im_data[0:im_height,0:im_width]
    # im_blueBand =  im_data[0,0:im_height,0:im_width]#获取蓝波段
    # im_greenBand = im_data[1,0:im_height,0:im_width]#获取绿波段
    # im_redBand =   im_data[2,0:im_height,0:im_width]#获取红波段
    #im_nirBand = im_data[3,0:im_height,0:im_width]#获取近红外波段
    return im_width,im_height,im_bands,HH_band
#读取图像===============================================================================
def tif2png(fileName):

    im_width,im_height,im_bands,HH_band = \
    readTif(fileName)
    bmin, bmax = minmaximg(im_width, im_height,HH_band)
    # bmin,bmax = minmaximg(im_width,im_height,im_blueBand)
    # gmin,gmax = minmaximg(im_width,im_height,im_greenBand)
    # rmin,rmax = minmaximg(im_width,im_height,im_redBand)
    #
    # im_blueBand=linearstretching(im_blueBand,bmin,bmax)
    # im_greenBand=linearstretching(im_greenBand,gmin,gmax)
    # im_redBand=linearstretching(im_redBand,rmin,rmax)
    #
    # img=cv2.merge([im_blueBand,im_greenBand,im_redBand])
    img = linearstretching(HH_band, bmin, bmax)
    return img

#===================================================================
path = 'F:\\test' # 文件存放路径 不要用中文路径opencv 不太支持
filename,numfile = getfilename(path)

num = 0 #计数 计一下完成了几个文件
for i in filename:

    #list = os.path.split(i) #分离目录与文件  list[0]目录 list[1]文件名

    img = tif2png(i)
    name=i.split('\\')[-1].split('.tiff')[0]
     # 根据\\分离 ,取最后 文件名 再分离 取文件名后相当于去掉.tiff 保留tiff 之前文件名
    savefile = path + '\\'+name + '.png'

    cv2.imwrite(savefile,img)
    print(savefile)
    num = num + 1
    print('TIFF 转 PNG 已完成 %d 个 共%d个'%(num,numfile))

