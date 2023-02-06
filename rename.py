
import os
import ffmpeg

videoSuffixSet = {"WMV","ASF","ASX","RM","RMVB","MP4","3GP","MOV","M4V","AVI","DAT","MKV","FIV","VOB"}
# 获取视频大小
getVideoResolutionCmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json output.mp4"
# 裁剪成1920宽
cutoutCmd = "ffmpeg -i tmp.mp4 -vf scale=1920:-1 output.mp4"
# 水印
watermarkCmd = ""

def getWidth(video):
    _prop = ffmpeg.probe(video)
    width =  _prop["streams"][0]["width"]
    return width

def getHeight(video):
    _prop = ffmpeg.probe(video)
    height =  _prop["streams"][0]["height"]
    return height

# 视频是否小于1920宽
def checkIs1920_CMD(video):
    width = getWidth(video)
    return width < 1920

# 裁剪
def cutOut_CMD(video):
    stream = ffmpeg.input(video).filter('scale')
    v = ffmpeg.filter(stream.video, "crop")
    width = getWidth(video)
    height = getHeight(video)
    ffmpeg.crop(stream, x = 0, y=height*0.13, w=width, h=height*0.55)
    waterMark_CMD(video)
    return 3
    
# 加水印
def waterMark_CMD(video):
    return 3


def process_video(video):
    if(checkIs1920_CMD(video)):
        cutOut_CMD(video)
    else:
        waterMark_CMD(video)

if __name__ == '__main__':
    dirStr = r'./tmp/' # 目录
    fileList = os.listdir(dirStr)
    for item in fileList:
        process_video(item)


    # tmpdir = 'tmp/output.mp4'
    # print(checkIs1920_CMD(tmpdir))
