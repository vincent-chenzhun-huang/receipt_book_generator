import os
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_file_names_in_dir():
    files = os.listdir()
    result = []
    for file in files:
        if not file.startswith('.'):
            result.append(file)
    return result


def extract_number(dir_name: str):
    i = 0
    str_num = ''
    while i < len(dir_name) and dir_name[i].isdigit():
        str_num += dir_name[i]
        i += 1
    return int(str_num)


def get_sorted_dir():
    return sorted(get_file_names_in_dir(), key=extract_number)


# if __name__ == '__main__':
#     os.chdir('Receipts')
#     print(get_file_names_in_dir())
#     sorted_dir = get_sorted_dir()
#     for directory in sorted_dir:
#         print(f'Going into reference dir {directory}...')
#         os.chdir(directory)
#         for img in get_file_names_in_dir():
#             if img.endswith('png') or img.endswith('jpg') or img.endswith('jpeg') or img.endswith('JPG') or img.endswith('JPEG'):
#                 print(f'converting {img} to pdf ...')
#                 opened_img = Image.open(img)
#                 opened_img = opened_img.convert('RGB')
#                 output_name = img.split('.')[0]
#                 opened_img.save(f'{output_name}.pdf', 'pdf', resolution=120.0, save_all=True)
#
#         os.chdir('..')
#     print("Succesfully create pdf receipts")

if __name__ == '__main__':

    os.chdir('Receipts')
    print(get_file_names_in_dir())
    sorted_dir = get_sorted_dir()
    writer = PdfFileWriter()
    page_num = 0
    for directory in sorted_dir:
        print(f'Going into reference dir {directory}...')
        os.chdir(directory)

        # TODO: Get the pdf files
        pdfs = []
        for file in get_file_names_in_dir():
            if file.endswith('.pdf'):
                pdfs.append(file)
        print(f'pdfs in dir {directory}: {pdfs}')

        for i, name in enumerate(pdfs):
            print(f'Adding {name} to pdf ...')
            receipt_pdf = PdfFileReader(open(name, 'rb'))
            if receipt_pdf.isEncrypted:
                try:
                    receipt_pdf.decrypt('')
                    print(f'File decrypted')
                except:
                    command = f"qpdf --password='' --decrypt {name} decrypted_{name}"
                    os.system(command)
                    print('File Decrypted (qpdf)')
                    receipt_pdf = PdfFileReader(open(f'decrypted_{name}'))
            writer.addPage(receipt_pdf.getPage(0))
            page_num += 1
            if i == 0:
                reference_number = extract_number(directory)
                print(f'Adding bookmark ...{reference_number}')
                writer.addBookmark(f'Reference #{reference_number}', pagenum=page_num - 1)
        os.chdir('..')

    os.system('touch receipts.pdf')
    with open('receipts.pdf', 'wb') as fh:
        writer.write(fh)

    print("Succesfully create pdf receipts")

# if __name__ == '__main__':
#     os.chdir('Receipts/1 (CHUANG - 02)')
#     print(get_file_names_in_dir())
#     im1 = Image.open('Screen Shot 2020-04-01 at 18.10.56.png')
#     im1 = im1.convert('RGB')
#     im1.save('receipts.pdf', 'pdf', resolution=10.0, save_all=True)
