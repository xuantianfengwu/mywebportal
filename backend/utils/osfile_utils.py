#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class OSFileUtils(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def __check_file_dir(self, file_path):
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    @staticmethod
    def mkdir(file_dir):
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    def save_file(self, file):
        self.__check_file_dir(self.file_path)
        file.save(self.file_path)

    def write(self, content, write_method='w'):
        self.__check_file_dir(self.file_path)
        with open(self.file_path, write_method) as f:
            f.write(content)

    def get_big_file_row_cnt(self):
        with open(self.file_path) as f:
            for i, l in enumerate(f):
                pass
        return i+1

    def write_pdf(self, pdf_output, file_path):
        self.__check_file_dir(self.file_path)
        with open(file_path, "wb") as f:
            pdf_output.write(f)
