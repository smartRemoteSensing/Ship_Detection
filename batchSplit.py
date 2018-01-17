import os
from PIL import Image

def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割, 请稍候...')

        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]

        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rowheight):
            for c in range(colwidth):
                box = (c * colnum, r * rownum, (c + 1) * colnum, (r + 1) * rownum)
                img.crop(box).save(os.path.join(dstpath, basename +'_' + str(c * colnum)+'_'+str(r*rownum) + '_' + str(num) + '.' + ext), ext)
                # crop(left, upper, right, lower) 名字中带有图像坐标
                num = num + 1

        print('图片切割完毕，共生成 %s 张小图片。' % num)
    else:
        print('不合法的行列切割参数！')

path = 'I:\GF3_train\split\\total'
pathdir=os.listdir(path)
num=0
for i in pathdir:
    src = path + '\\'+i
    if os.path.isfile(src):
        redir=path +'\\' + str(num)
        dstpath =os.mkdir(redir)
        num+=1
        if (dstpath == '') or os.path.exists(redir):
            row = 100
            col = 100
            if row > 0 and col > 0:
                splitimage(src, row, col, redir)
            else:
                print('无效的行列切割参数！')
        else:
            print('图片输出目录 %s 不存在！' % dstpath)
    else:
        print('图片文件 %s 不存在！' % src)
