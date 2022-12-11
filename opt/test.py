import os
import zipfile
from pathlib import Path
import shutil
import csv
from pdf2image import convert_from_path

# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)


"""
pdf_path - 画像にするpdf のパス
img_dir - 出力する画像のディレクトリ
dpi - 画像の精密度 (どうでもいい..)
"""
def subprint_pdf2img(pdf_path, img_dir, zip_path_no_extension, backup_dir, dpi=150):
    pdf_path = Path(pdf_path)
    pages = convert_from_path(str(pdf_path), dpi)

    image_dir = Path(img_dir) #保存するディレクトリ
    for i, page in enumerate(pages):
        if (i >= 2):
            file_name = pdf_path.stem + "_{0:03}".format(i + 1) + ".jpeg"
            image_path = image_dir / file_name
            # JPEGで保存
            page.save(str(image_path), "JPEG")


    shutil.move(pdf_path, backup_dir)
    # zip にする
    shutil.make_archive(zip_path_no_extension, 'zip', root_dir='./img')

    #imgフォルダの中身を空にする
    shutil.rmtree(img_dir)
    os.mkdir(img_dir)
    return


def getCSV_from_img(front_zip, back_zip, csv_path):
    zip_f = zipfile.ZipFile(front_zip)
    lst_f = zip_f.namelist()

    zip_b = zipfile.ZipFile(back_zip)
    lst_b = zip_b.namelist()

    csv_list = []
    for (front_img_path, back_img_path) in zip(lst_f, lst_b):
        print(front_img_path)
        csv_list.append([
            '<img src="{}">'.format(front_img_path),
            '<img src="{}">'.format(back_img_path),
        ])
    with open(csv_path, 'w') as f:
       writer = csv.writer(f)
       writer.writerows(csv_list)
    return


subprint_pdf2img('./pdf/QA_C_subprint_ver_space_220525.pdf', './img', './save/front', './backup_pdf')
subprint_pdf2img('./pdf/QA_C_subprint_220525.pdf', './img', './save/back', './backup_pdf')
getCSV_from_img('./save/front.zip', './save/back.zip', './save/list.csv')
