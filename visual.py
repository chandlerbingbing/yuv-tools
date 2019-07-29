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
        yuv = YCbCr(filename=contain[i][0], filename_diff=contain[i][1], width=arg.width, height=arg.height, yuv_format_in=arg.yuv_format_in)
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

def main():
    args = parse_args()
    contain = []
    for i in range(len(args.input_test)):
        compare_test = find_all_yuv(args, args.input_test[i], args.grouptag[i])
        contain.append(compare_test)
    # for i in range(len(args.input_test)):
    #     inputfile = args.input_test[i].split(',')
    #     outputfile = args.compare_test[i].split(',')
    #     inputfile = [args.inputpath + p for p in inputfile]
    #     outputfile = [args.inputpath + p for p in outputfile]
    #     contain.append([inputfile, outputfile])

    t1 = time.clock()
    plot_psnr_all(args, contain)
    t2 = time.clock()
    print "\nTime: ", round(t2 - t1, 4)

def find_all_yuv(arg, inputfile, grouptag):
    workbook = xlrd.open_workbook(arg.inputpath)
    worksheet = workbook.sheet_by_index(0)
    order = 0
    while order < worksheet.nrows:
        if worksheet.cell(order, 0).value == inputfile:
            break
        order = order+1
    Originalyuvpath = [str(worksheet.cell(order, 3).value)]
    encodeyuvpath = []
    encodeyuvbitrate = []
    order = 0
    while order < worksheet.nrows:
        if worksheet.cell(order, 7).value == inputfile and worksheet.cell(order, 8).value == grouptag:
            encodeyuvpath.append(str(worksheet.cell(order, 3).value))
            encodeyuvbitrate.append(worksheet.cell(order, 6).value)
            linetag = str(worksheet.cell(order, 8).value + '_' + worksheet.cell(order, 7).value)
        order = order+1
    return [Originalyuvpath, encodeyuvpath, encodeyuvbitrate, linetag]

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
