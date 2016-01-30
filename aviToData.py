__author__ = 'FDra'

###
#opencvによる動画データへのアクセス方法。
#手順
#１、openCVモジュールのcv2.VideoCaptureによって、対象動画のビデオキャプチャ構造体を生成。
#２、構造体に対して、read()メソッドを使用することで、フレームごとの静止画像ファイルにアクセス。
#３、例： capをビデオキャプチャ構造体として、frame = cap.read()とすると、frameは、[True, Array]を返す。
#４、frameのArrayは、画素データ。配列順序としてはArray[heightNumber,widthNumber]
#５、例：frame[1][0][0] -> 座標(0,0)のピクセルの画素データにアクセス。画素データはbgrで３つ入っている。

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

cap=cv2.VideoCapture('[fileURL]')

frameNum    = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
frameWidth  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
rgbNum      = 3

#frameImg = cap.read() #(True,array([[[]]]))
aviMatrixData = np.empty([frameNum, frameHeight, frameWidth, rgbNum])

counter = 0

while (counter < frameNum):
    aviMatrixData[counter] = cap.read()[1]
    counter += 1
    cap.grab()  #cap.read()で読み出す構造体のframeを1進める。
###
#windowに表示
#

###
#PCR解析
#

#解析し易いようにデータの配列を転置する。これにはtransposeメソッドを用いる。
#例：行列Aが任意の値で要素数(3,4,5)の３次元配列だとする。
#これを、(4,5,3)の行列Bに転置させたい場合、B = A.transpose(1,2,0)とすればよい。
#reshapeメソッドとは異なることに注意。
#横軸：変数、縦軸：サンプル数
#transpose前のaviMatrixDataの配列順所 -> (frameNum, frameHeight, frameWidth, rgbNum)
#transpose後 -> (frameNum, frameWidth, frameHeight, rgbNum)
#aviMatrixData = aviMatrixData.transpose(0, 2, 1, 3)

#解析範囲確認用データの生成
#testImgには、各x座標（画像幅）の輝度値スペクトル平均がフレームごと（y座標）に代入される。
#このtestImgを描画し、どの場所が一番PCRにとって都合が良いかをとりあえず判断する。
aviMatrixData = aviMatrixData.transpose(0, 2, 1, 3)
testImg = np.empty([frameNum, frameWidth])

for k in range(frameNum):
    for i in range(frameWidth):
        testImg[k][i] = np.average(aviMatrixData[k][i])

#tmpDt = np.delete(aviMatrixData, np.s_[0:2], 3)

####
#PCR用の3次元データ行列Dtの作成。Dt(frameNum, frameWidth, frameHeight) = 横：x座標、縦：波長
#

Dt = np.empty([frameWidth, frameHeight])
#k = y座標
k = 130

for i in range(frameWidth):
    for j in range(frameHeight):
        Dt[i][j] = aviMatrixData[k][i][j][0]


#作成したreflectanceデータの呼び出し
reflectance99 = np.loadtxt("[fileURL]",delimiter=",")


#エッジカット


###
#解析したい場所をframeWidth[70:256]の範囲で指定。実際のデータは70〜255まで
#[a:b]とあった場合、実際のデータはa~b-1。bは含まれないことに注意。
#その配列データをtmpDtとすると、求めたい反射率スペクトルrefSpecは、
#refSpec = tmpDt / reflectance99
#100-130
#130-170
#170-200
tmpDt = np.delete(Dt, np.s_[:100], 0)     #frameWidthの最初のx軸から100までを削除
tmpDt = np.delete(tmpDt, np.s_[100:], 0)  #上記削除したデータから、右端を削除
tmpDt = np.delete(tmpDt, np.s_[20:70], 0) #布として重なった部分を削除
tmpDt = Dt[:,0:255]                       #カンマで行と列を区別する。Dt.shape = (320,300)だとしたら、tmpDt = (320,255)
###
#グラフ描画
#


#数値データとして
plt.plot(Dt)
plt.show()

#画像データとして
TDt = Dt.transpose()

plt.imshow(TDt, cmap = cm.Greys_r)
plt.show()

fixDt = TDt

###
#csvファイル読み込み
#

reflectance99 = np.loadtxt("[fileURL]",delimiter=",")

###
#CSVファイルに書き込み
#

#R解析用のため一列目に番号を入れる。
a = np.arange(1,121,1)
a = a.reshape('行数', 1)
tmpDt = np.hstack((a, '対象データ'))

#解析用データの保存
np.savetxt("test06.csv", tmpDt, fmt="%.0f",delimiter=",")

##3D描画
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X ** 2 + Y ** 2)
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hot)
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.cm.hot)
ax.set_zlim(-2, 2)

plt.show()

##3Dver2

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

xs=numpy.random.rand(1,100)
ys=numpy.random.rand(1,100)
zs=numpy.random.rand(1,100)


ax.scatter3D(xs, ys, zs)
plt.show()

