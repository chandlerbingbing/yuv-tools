YCbCr (YUV)
===========

Tools for various operations on raw YCbCr video files.
http://en.wikipedia.org/wiki/YCbCr

### ycbcr.py - is the main class that supports the following formats:

* IYUV
* UYVY
* YV12
* NV12
* YVYU
* YUY2
* 422

### **Supported operations**
* PSNR calculations, during different Bitrates YUV files
* multi inputfile according excel configture file

### **Flowchart**
[flow](https://github.com/chandlerbingbing/yuv-tools/FlowChart.png)
### **purpose**: show Transcode quality 

### **Install direction**
#### sudo apt update
       `sudo apt upgrade`
       `#installing python 2.7 and pip for it`
       `sudo apt install python2.7 python-pip`
       `pip install numpy`
       `pip install <other missing moduel>`

### Usage
-----
	$ ./visual.py -I /home/cxh/code/yuv-tools/testsheet.xlsx -P 10_.yuv 10_hecv.yuv -W 4096 -H 2160 -C YV12 -G hevc01 hevc02

-----

### **usage:** 
       visual.py [-h] [-I [INPUTPATH]] 
                 [-pi INPUT_TEST [INPUT_TEST ...]]
                 [-W WIDTH] [-H HEIGHT]
                 [-C {IYUV,UYVY,YV12,YVYU,YUY2,422}]
                 [-M BIT_RATE [BIT_RATE ...]]
                 [-G GROUPTAP [GROUPTAP ...]]

      optional arguments:
                 -h, --help   show this help message and exit
                 -I [INPUTPATH]   the excel configure file path
                 -pi INPUT_TEST [INPUT_TEST ...]
                  the Original yuv file name, you can put plenty,and
                  separate by dot
                 -W WIDTH,           width
                 -H HEIGHT,          height
                 -C          {IYUV,UYVY,YV12,YVYU,YUY2,422}, 
                 yuv_format_in {IYUV,UYVY,YV12,YVYU,YUY2,422} type
                 -M BIT_RATE [BIT_RATE ...]
                 bitrate with compare yuv
                 -G  --grouptap GROUPTAP [GROUPTAP ...]
                     different transcoding yuv
-----
[configure](https://github.com/chandlerbingbing/yuv-tools/configure.png)
Screenshots
-----------

Here's one of the output from visual.py

