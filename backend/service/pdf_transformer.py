#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
from PyPDF2 import PdfFileReader, PdfFileWriter
from ..utils.osfile_utils import OSFileUtils

class PDFTransformer(object):
    """ PDF 转化类 """
    def __init__(self, pdf_files):
        """ 初始化pdf_f/pdf_name/output_path等信息 """
        self.pdf_read_dir = os.path.join(".", 'backend', 'static', 'upload', 'pdf_tools')
        self.output_dir = os.path.join(".", "backend", "static", "output", "pdf_tools", "PDF_Transformer")
        self.pdf_files = pdf_files if type(pdf_files) == list else [pdf_files]

    def _read_in_pdf(self, pdf_file):
        """ 预加载pdf_f和pdf_name """
        if type(pdf_file) == str:
            f = open(os.path.join(self.pdf_read_dir, pdf_file), 'rb')
            pdf_f = PdfFileReader(f)
            pdf_name = pdf_file
        else:
            f = pdf_file
            pdf_f = PdfFileReader(f)
            pdf_name = '{}.pdf'.format(os.urandom(1000))
        pagecnt = pdf_f.getNumPages()
        return f, pdf_f, pdf_name, pagecnt

    def operate(self, operate_type, params):
        """ PDF Transformer 执行入口 """
        if operate_type == '1':
            # Del Specific Page
            to_del_pages = [int(i) for i in params['to_del_page'].split(',')]
            self.del_specific_pages(self.pdf_files, to_del_pages, self.output_dir)
        run_res = {'is_success': True,
                   'operate_type': operate_type,
                   'operate_files': self.pdf_files}
        return run_res

    def del_specific_pages(self, pdf_files, del_page_lst, output_dir):
        """ 处理旧的pdf_f， 删除 del_index_lst 里页码的内容，并生成新文件到output_dir """
        # 兼容传入的f和f_name
        for pdf_f in pdf_files:
            f, pdf_f, pdf_name, pagecnt = self._read_in_pdf(pdf_f)
            # 若有-1，则在del_page_lst中转为pagecnt
            if -1 in del_page_lst:
                del_page_lst.remove(-1)
                del_page_lst.append(pagecnt)
            # 生成新文件
            output_path = os.path.join(output_dir, pdf_name)
            pdf_output = PdfFileWriter()
            try:
                for page_idx in range(pagecnt):
                    if (page_idx+1) in del_page_lst:
                        continue
                    pdf_output.addPage(pdf_f.getPage(page_idx))
                OSFileUtils(output_path).write_pdf(pdf_output, output_path)
            finally:
                f.close()
        return True

    def get_result_file_path(self, oper_type):
        """ 下载单个结果文件 """
        res = {
            'res_file_dir':  os.path.abspath(self.output_dir),
            'res_file_name': self.pdf_files[0]
        }
        return res

    def get_result_files_path(self, oper_type, download_type='zip'):
        """ 下载多个结果文件， download_type可指定压缩形式 """
        # 压缩self.pdf_files进download_type文件
        zip_file_name = '{}.{}'.format(oper_type, download_type)
        with zipfile.ZipFile(os.path.join(self.output_dir, zip_file_name), 'w') as zip_file:
            for pdf_file in self.pdf_files:
                pdf_file_path = os.path.join(os.path.abspath(self.output_dir), pdf_file)
                zip_file.write(pdf_file_path, arcname=pdf_file, compress_type=zipfile.ZIP_DEFLATED)
        # 返回
        res = {
            'res_file_dir':  os.path.abspath(self.output_dir),
            'res_file_name': zip_file_name,
            'res_file_type': 'application/zip'
        }
        return res
