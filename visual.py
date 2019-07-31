#!/usr/bin/env python

"""
Visually show various metrics between two YCbCr sequences
using matplotlib
"""

import argparse
import time
import os
import xlrd
# import xlwt

import numpy as np
import matplotlib.pyplot as plt
from ycbcr import YCbCr


def create_title_string(title, subtitle):
    """
    Helper function to generate a nice looking
    title string
    """
    return "{} {}\n{}".format(
        os.path.basename(title),
        'VS.',
        " ".join([os.path.basename(i) for i in subtitle]))


def plot_psnr(arg):
    """
    PSNR
    """
    t, st = vars(arg)['filename'], vars(arg)['filename_diff']
    for f in st:
        vars(arg)['filename_diff'] = f
        yuv = YCbCr(**vars(arg))

        psnr = [p[3] for p in yuv.psnr()]

        N = len(psnr[:-2])
        ind = np.arange(N)  # the x locations for the groups

        # To get a uniq identifier
        plt.plot(ind, psnr[:-2], 'o-', label=f[-10:-8])

        del yuv

    plt.legend()
    plt.title(create_title_string(t, st))
    plt.ylabel('weighted dB')
    plt.xlabel('frame')
    plt.grid(True)

    plt.show()
def plot_psnr_all(arg, contain):
    """
    PSNR, all planes
    """
    # ind = arg.Bit_rate  # the x locations for the groups
    plt.figure()
    plt.title(create_title_string('PSNR', 'Bitrate'))
    for i in range(len(contain)):
        yuv = YCbCr(filename=contain[i][0], filename_diff=contain[i][1], width=arg.width, height=arg.height, yuv_format_in=arg.yuv_format_in, bitdepth=contain[i][4])
        for infile in range(len(contain[i][0])):
            point = []
            ind = []
            for diff_file in range(len(contain[i][1])):
                temp = yuv.psnr(diff_file, infile)
                point.append(temp[0])
                ind.append(contain[i][2][diff_file])
            plt.plot(ind, point, 'o-', label=contain[i][3])

    plt.legend()
    plt.ylabel('Psnr-dB')
    plt.xlabel('Bitrate')
    plt.grid(True)
    plt.show()

def plot_psnr_frames(arg, contain):
    """
    PSNR, all planes
    """
    # ind = arg.Bit_rate  # the x locations for the groups
    plt.figure()
    plt.title(create_title_string('PSNR', 'Bitrate'))
    for i in range(len(contain)):
        yuv = YCbCr(filename=contain[i][0], filename_diff=contain[i][1], width=arg.width, height=arg.height, yuv_format_in=arg.yuv_format_in, bitdepth=contain[i][4])
        for infile in range(len(contain[i][0])):
            point = []
            for diff_file in range(len(contain[i][1])):
                temp = [p for p in yuv.psnr_all(diff_file, infile)]
                ind = np.arange(len(temp))
                plt.plot(ind, [i[0] for i in temp], 'o-', label='hevc'+str(diff_file))
    plt.legend()
    plt.ylabel('Psnr-dB')
    plt.xlabel('Bitrate')
    plt.grid(True)
    plt.show()

def find_all_yuv_fromdir(arg, inputfile,grouptag):
    path = arg.inputpath
    dirs = os.listdir(path)
    Originalyuvpath = []
    for file in dirs:
        if file == inputfile:
            Originalyuvpath.append(os.path.join(path, file))
            break
    encodeyuvpath = []
    for tag in range(len(grouptag)):
        for file in dirs:
            if file == grouptag[tag]:
                encodeyuvpath.append(os.path.join(path, file))
                break
    return [Originalyuvpath, encodeyuvpath, arg.Bit_rate, inputfile]

def find_all_yuv(arg, inputfile, grouptag):
    workbook = xlrd.open_workbook(arg.inputpath)
    worksheet = workbook.sheet_by_index(0)
    y = 0
    titlename = {}
    while y < worksheet.ncols:
        titlename[str(worksheet.cell(0, y).value)] = y
        y += 1
    order = 0
    while order < worksheet.nrows:
        if worksheet.cell(order, 0).value == inputfile:
            break
        order = order+1
    Originalyuvpath = [str(worksheet.cell(order, 3).value)]
    encodeyuvpath = []
    encodeyuvbitrate = []
    encodeyuvbitdepth = 8
    order = 0
    while order < worksheet.nrows:
        if worksheet.cell(order, 7).value == inputfile and worksheet.cell(order, 8).value == grouptag:
            encodeyuvpath.append(str(worksheet.cell(order, 3).value))
            encodeyuvbitrate.append(worksheet.cell(order, 6).value)
            linetag = str(worksheet.cell(order, 8).value + '_' + worksheet.cell(order, 7).value)
            encodeyuvbitdepth = worksheet.cell(order, 5).value
        order = order+1
    return [Originalyuvpath, encodeyuvpath, encodeyuvbitrate, linetag, encodeyuvbitdepth]

def ten2eight(filename, filename_out):
    """
    10 bpp -> 8 bpp
    """
    fd_i = open(filename, 'rb')
    fd_o = open(filename_out, 'wb')

    while True:
        chunk = np.fromfile(fd_i, dtype=np.uint8, count=8192)
        chunk = chunk.astype(np.uint)
        if not chunk.any():
            break
        data = (2 + (chunk[1::2] << 8 | chunk[0::2])) >> 2

        data = data.astype(np.uint8, casting='same_kind')
        data.tofile(fd_o)
    fd_i.close()
    fd_o.close()

def main():
    args = parse_args()
    contain = []
    for i in range(len(args.input_test)):
        compare_test = find_all_yuv(args, args.input_test[i], args.grouptag[i])
        contain.append(compare_test)
    t1 = time.clock()
    plot_psnr_all(args, contain)
    # plot_psnr_frames(args, contain)
    t2 = time.clock()
    print "\nTime: ", round(t2 - t1, 4)
    # for i in range(len(args.inputpath)):
    #     ten2eight(args.inputpath[i], args.grouptag[i])

def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-I', '--filename', type=str, help='filename', nargs='+')
    # we need modify this to read excel path
    parser.add_argument('-I', '--inputpath', type=str, help='the excel configure file path', nargs='?')
    # parser.add_argument('-g', '--testgroup', type=int, help='testgroup_number',  nargs='?')
    parser.add_argument('-P', '--input_test', type=str, help='the Original yuv file name, you can put plenty,and separate by dot', nargs='+', required=False)
    parser.add_argument('-po', '--compare_test', type=str, help='compare_test_plan',  action='append', required=False)
    parser.add_argument('-W', '--width', type=int, required=False, help='width')
    parser.add_argument('-H', '--height', type=int, required=False, help='height')
    parser.add_argument('-C', '--yuv_format_in', choices=['IYUV', 'UYVY', 'YV12', 'YVYU', 'YUY2', '422'], required=False, help='type')
    parser.add_argument('-M', '--Bit_rate', type=int, help='bitrate with compare yuv', nargs='+')
    parser.add_argument('-G', '--grouptag', type=str, help='different transcoding yuv', nargs='+')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
