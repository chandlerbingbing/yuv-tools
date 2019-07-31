import os
import argparse
import xlwt
import xlrd
import re
def check_bit(filename):
    bit_rate = 0
    if re.search('0.5M', filename):
        bit_rate = 500
    elif re.search('2M', filename):
        bit_rate = 2000
    elif re.search('4.5M', filename):
        bit_rate = 4500
    elif re.search('13M', filename):
        bit_rate = 13000
    else:
        return
    return bit_rate

def parse_info(filename):
    info = []
    if re.search('8k', filename) and re.search('10hevc', filename) and re.search('hevc', filename) and re.search('Origin', filename):
        return [7680, 3840, 'YV12', 10, 'null', 'Original', 'null']
    if re.search('8k', filename) and re.search('10hevc', filename) and re.search('hevc', filename):
        bit_rate = check_bit(filename)
        if bit_rate:
            return [7680, 3840, 'YV12', 10, bit_rate, '10_frames_8k10hevc_Origin.yuv', '8k10hevc']
        else:
            return
    if re.search('8k', filename) and re.search('hevc', filename) and re.search('Origin', filename):
        return [7680, 3840, 'YV12', 8, 'null', 'Original', 'null']
    if re.search('8k', filename) and re.search('hevc', filename):
        bit_rate = check_bit(filename)
        if bit_rate:
            return [7680, 3840, 'YV12', 8, bit_rate, '10_frames_8khevc_Origin.yuv', '8khevc']
        else:
            return
    if re.search('hevc', filename) and re.search('Origin', filename):
        return [4096, 2160, 'YV12', 8, 'null', 'Original', 'null']
    if re.search('hevc', filename):
        bit_rate = check_bit(filename)
        if bit_rate:
            return [4096, 2160, 'YV12', 8, bit_rate, '10_frames_hevc_Origin.yuv', 'hevc']
        else:
            return
    if re.search('10_frames_', filename) and re.search('Origin', filename):
        return [4096, 2160, 'YV12', 8, 'null', 'Original', 'null']
    if re.search('10_frames_', filename):
        bit_rate = check_bit(filename)
        if bit_rate:
            return [4096, 2160, 'YV12', 8, bit_rate, '10_frames_Origin.yuv', '264']
        else:
            return
    return

def Buildexcel(yuv_name_path):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('yuvpool_info', cell_overwrite_ok=True)
    row0 = ['name', 'width', 'height', 'path', 'type', 'bit_depth', 'bit_rate', 'Original yuv', 'grouptag']
    for i in range(len(row0)):
        worksheet.write(0, i, row0[i])
    row = 1
    for yuv in yuv_name_path:
        info = parse_info(yuv[1])
        if info:
            info.insert(0, yuv[1])
            info.insert(3, yuv[0])
            for i in range(len(row0)):
                worksheet.write(row, i, info[i])
            row += 1
        else:
            continue
    workbook.save('testauto.xls')
    return 1

def find_all_yuv(arg):
    path = arg.yuvpool_dir
    dirs = os.listdir(path)
    yuvpool = []
    for filename in dirs:
        name, suf = os.path.splitext(filename)
        if suf == arg.suffix:
            yuvpool.append([os.path.join(path, filename), filename])
    ret = Buildexcel(yuvpool)
    return ret

def parse_args():
    parse = argparse.ArgumentParser(description='Build excel form yuv pool')
    parse.add_argument('-r', '--resolution', help='get resolution', nargs='*')
    parse.add_argument('-c', '--codec', help='get codec name', nargs='?', default='_')
    parse.add_argument('-i', '--yuvpool_dir', type=str)
    parse.add_argument('-s', '--suffix', help='search by suffix', type=str, required=True)
    args = parse.parse_args()
    return args

def main():
    args = parse_args()
    yuvpool = find_all_yuv(args)
    if yuvpool:
        print 'write excel successful!!'

if __name__ == '__main__':
    main()