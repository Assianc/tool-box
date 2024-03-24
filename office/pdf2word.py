import os
import sys
from pdf2docx import parse
from docx2pdf import convert


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


def convert_to_pdf(file_path):
    directory = os.path.dirname(file_path)
    file = os.path.basename(file_path)
    file_name = os.path.splitext(file)[0]
    file_extension = os.path.splitext(file)[1]

    if file_extension == ".docx":
        docx_file_path = os.path.join(directory, file)
        pdf_file_path = os.path.join(directory, f"{file_name}.pdf")
        convert(docx_file_path, pdf_file_path)
        print(f"Successfully converted '{file}' to '{file_name}.pdf'.")
        return pdf_file_path
    else:
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        file_extension = os.path.splitext(file_path)[1]

        if file_extension == ".pdf":
            convert_to_docx(file_path)
        elif file_extension == ".docx":
            convert_to_pdf(file_path)
        else:
            print("Unsupported file format. Please provide a PDF or DOCX file.")
    else:
        print("Please provide a file path as a command-line argument.")