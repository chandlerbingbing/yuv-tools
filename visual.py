#!/usr/bin/env python

"""
Visually show various metrics between two YCbCr sequences
using matplotlib
"""

import argparse
import time
import os

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

def plot_psnr_all(arg):
    """
    PSNR, all planes
    """
    yuv = YCbCr(**vars(arg))

    plt.figure()
    plt.title(create_title_string('PSNR', 'Bitrate'))
    # choice codec logic here.actually a args plan
    for infile in range(len(arg.filename)):
        y = []
        for diff_file in range(len(arg.filename_diff)):
            # temp = [p for p in yuv.psnr(diff_file, infile)]
            temp = [yuv.psnr(diff_file, infile)]
            y.append(temp[-1][-1])
            # y.append(temp[3][-1])
        ind = [0.4, 2, 4.5, 13]  # the x locations for the groups
        plt.plot(ind, y, 'o-', label='Frame'+str(infile))

    plt.legend()
    plt.ylabel('Psnr-dB')
    plt.xlabel('Bitrate')
    plt.grid(True)

    plt.show()

def main():
    args = parse_args()
    
    t1 = time.clock()
    plot_psnr_all(args)
    t2 = time.clock()
    print "\nTime: ", round(t2 - t1, 4)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--filename', type=str, help='filename', nargs='+')
    #parser.add_argument('-I', '--input', type=str, help='filename', action='append', required=True)
    parser.add_argument('-W', '--width', type=int, required=True)
    parser.add_argument('-H', '--height', type=int, required=True)
    parser.add_argument('-C', '--yuv_format_in', choices=['IYUV', 'UYVY', 'YV12', 'YVYU', 'YUY2', '422'], required=True)
    parser.add_argument('-O', '--filename_diff', type=str, help='filename', nargs='+')
    #parser.add_argument('-O', '--output', type=str, help='filename', action='append', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
