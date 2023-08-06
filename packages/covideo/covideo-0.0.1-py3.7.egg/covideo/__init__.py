#!/usr/bin/env python3
# encoding=utf-8

import re
import sys
import os
from optparse import OptionParser

def clip_path(path):
    # path is absolute
    print("Parsing " + path + "...")
    start_time = input('请输入剪切起始时间：')
    stop_time = input('请输入剪切结束时间：')
    output_file = path.strip(".mp4") + '-' + start_time + '-' + stop_time + ".mp4"
    # 需要默认 cd 到 ffmpeg 的项目下：os.chdir(ffmpeg_dir)
    os.system("ffmpeg -ss {2} -to {3} -accurate_seek -i {0} -c copy -avoid_negative_ts 1 {1}".format(path,output_file,start_time,stop_time))

def clip_dir(directory):
    for file in os.listdir(directory):
        if (file.endswith(".mp4")): #or .avi, .mpeg, whatever.
            clip_path(file)

def process(opt):
    # clip, merge = opt.clip, opt.merge
    clip = opt.clip
    if clip:
        # clip is a file path
        if os.path.isfile(clip):
            clip_path(clip)
            exit("视频剪切成功！请前往源视频目录下查看剪切的视频。")
        elif os.path.isdir(clip):
            clip_dir(clip)
            exit("视频剪切成功！请前往源视频目录下查看剪切的视频。")
        else:
            print('Please give me a file path or a directory path.')
            exit(1)

    # elif merge:
    #     if os.path.isfile(merge):

    #     elif os.path.isdir(merge):

    #     else:
    #         print('Please specify a file path or a directory path as the argument.')
    else:
        print('Please specify an option. Execute `cocheck -h` to list all options.')

def exe_main():
    parser = OptionParser(version="%prog 0.0.1")
    parser.set_defaults(verbose=True)
    # parser.add_option("-a", "--all", dest="all",
    #                   help="Checks unclosed tags, code blocks, copyable snippets, etc.", metavar="ALL")
    parser.add_option("-c", "--clip", dest="clip", type="string",
                      help="Clip mp4 videos", metavar="CLIP")
    # parser.add_option("-m", "--merge", dest="merge", type="string",
    #                   help="Merge mp4 videos", metavar="MERGE")
    options, args = parser.parse_args()
    process(options)