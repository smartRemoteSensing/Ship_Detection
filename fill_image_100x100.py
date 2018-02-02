
import os
import cv2


#重采样 100*100 样例 完成
# filepath = 'D:/data/fill/9.tif'
# img = cv2.imread(filepath)
# img_100x100 = cv2.resize(img,(100,100),interpolation=cv2.INTER_LINEAR)
# cv2.imwrite('D:/data/fill/9.png',img_100x100)
#
# cv2.imshow('image',img_100x100)
# cv2.waitKey(0)
#重采样 100*100 样例 完成


def Tiff2Png_resize(filepath):
    img = cv2.imread(filepath)
    # if (img == None):
    #     return
    img_100x100 = cv2.resize(img, (100, 100), interpolation=cv2.INTER_LINEAR)
    return img_100x100


import os

####只读取8位tif 不读取16位
def getfilename(path):
    pathdir = os.listdir(path)  # 文件名保存为列表
    # dir=pathdir # dir保存完整文件名路径
    dir = []
    j = 0  # 文件计数
    for filename in pathdir:
        if (filename.find('-16') == -1):
            dir.append(path + '\\' + filename)
            j = j + 1
    return dir, j + 1  # 返回绝对路径文件名 和文件个数


# 获取文件名绝对路径=========================

# 获取文件名绝对路径=========================

path = 'D:/20180125testGF3/output/20180125201743/slice/large' # 文件存放路径 不要用中文路径opencv 不太支持
filename,numfile = getfilename(path)
print(numfile)
savepath = 'D:/20180125testGF3/temp/'
num = 0 #计数 计一下完成了几个文件
for i in filename:

    list = os.path.split(i) #分离目录与文件  list[0]目录 list[1]文件名
    print(i)
    img = Tiff2Png_resize(i)
    l = list[1].split('.tif')  # 分离后缀 相当于去掉.tiff 保留tiff 之前文件名

    fn = l[0] +'.png'
    fn = savepath +fn
    cv2.imwrite(fn,img)
    print(fn)
    num = num + 1
    print('TIFF 转 PNG 已完成 %d 个 共%d个'%(num,numfile))
