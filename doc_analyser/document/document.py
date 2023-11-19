from doc_analyser.settings import FULL_DOCS_PATH
from doc_analyser.to_text.pdf import convert_pdf_to_txt
from doc_analyser.to_text.pptx import convert_pptx_to_txt
from doc_analyser.to_text.doc import convert_docx_to_txt
from doc_analyser.to_text.xlsx import convert_xlsx_to_txt

import os
from shutil import copyfile
import uuid
import time

class TempDocument(object):

    file_path_to_text = None
    file_path_to_pdf = None
    extension = None

    def __init__(self, request_file=None, file_ext=None, file_path=None):
        if request_file and file_ext:
            self._get_file_extension(file_ext)
            self._create_temp_paths()
            self._create_temp_files(request_file)

        elif file_path:
            self._wait_for_file_copy(file_path)

        elif file_ext:
            self._get_file_extension(file_ext)

    def _create_temp_paths(self):
        self.file_path_to_text = FULL_DOCS_PATH + str(uuid.uuid1()) + '_to_text' + self.extension
        self.file_path_to_pdf = FULL_DOCS_PATH + str(uuid.uuid1()) + '_to_pdf' + self.extension
    
    def _create_temp_files(self, file):
        file.save(self.file_path_to_text)
        self._wait_for_file_copy(self.file_path_to_text)

        copyfile(self.file_path_to_text, self.file_path_to_pdf)
        self._wait_for_file_copy(self.file_path_to_pdf)


    def _get_file_extension(self, ext):
        if ext == 'PDF':
            self.extension = '.pdf'
        elif ext == 'Planilha':
            self.extension = '.xlsx'
        elif ext == 'PPTX':
            self.extension = '.pptx'
        else:
            self.extension = '.docx'
    
    def _wait_for_file_copy(self, file_path):
        temp_size_diff = 1
        current_temp_size = 0

        while temp_size_diff > 0:
            time.sleep(1)
            size = os.stat(file_path).st_size
            temp_size_diff = size - current_temp_size
            current_temp_size = size

    def remove_file(self, file_path):
        if type(file_path) == list:
            for f in file_path:
                if f and os.path.exists(f):
                    os.remove(f)
        elif type(file_path) == str:
            if os.path.exists(file_path):
                    os.remove(file_path)

    def convert_to_text(self, file_path):
        doc_text = ''

        if self.extension == '.pdf':
            doc_text = convert_pdf_to_txt(file_path)

        elif self.extension == '.pptx':
            doc_text = convert_pptx_to_txt(file_path)

        elif self.extension == '.xlsx':
            doc_text = convert_xlsx_to_txt(file_path)

        elif self.extension == '.docx':
            doc_text = convert_docx_to_txt(file_path)

        return doc_text