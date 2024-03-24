import os
import sys
from pdf2docx import parse


def convert_to_docx(file_path):
    directory = os.path.dirname(file_path)
    file = os.path.basename(file_path)
    file_name = os.path.splitext(file)[0]
    file_extension = os.path.splitext(file)[1]

    if file_extension == ".pdf":
        pdf_file_path = os.path.join(directory, file)
        docx_file_path = os.path.join(directory, f"{file_name}.docx")
        parse(pdf_file_path, docx_file_path, start=0, end=None)
        print(f"Successfully converted '{file}' to '{file_name}.docx'.")
        return docx_file_path
    else:
        return None


convert_to_docx(sys.argv[1])
