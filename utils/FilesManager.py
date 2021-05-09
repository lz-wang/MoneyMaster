#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: FilesManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午11:40

import chardet


def get_file_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']
