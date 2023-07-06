#
# Reference: https://github.com/imClumsyPanda/langchain-ChatGLM/blob/master/loader/pdf_loader.py

import uuid, os
import fitz
from paddleocr import PaddleOCR


################# Config ########################
# OCR 时是否使用 GPU， 需要安装对应版本的 PaddlePaddle 平台
USE_GPU = False
# 默认的临时文件夹
DEFAULT_TMP_FILES = "tmp_files"
# 是否打印处理时的消息提示（这里不使用 logging 模块，是因为 paddleocr 使用了 logging， 而 paddleocr 的日志很恼人）
PRINT_LOG = True


def pdf_ocr_txt(
    filepath: str, dir_path: str = DEFAULT_TMP_FILES, lang_code="ch"
) -> str:
    """
    从 PDF 文件中提取文本并将其保存为 TXT 文件。

    参数:
        filepath (str): PDF 文件的路径。
        dir_path (str, 可选): 临时文件存储的目录路径。默认为 DEFAULT_TMP_FILES。
        lang_code (str, 可选): 进行 OCR 时的目标语言。默认时 ch (中英双语)。
            语言语言代码的含义详见：https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/multi_languages.md#%E8%AF%AD%E7%A7%8D%E7%BC%A9%E5%86%99
            可供选择的 lang_code 包括：
            中文和英文：'ch'
            英文：'en'
            韩语：'korean'
            日语：'japan'
            繁体中文：'chinese_cht'
            泰米尔文：'ta'
            泰卢固文：'te'
            卡纳达文：'ka'
            拉丁文：'latin'
            阿拉伯字母：'arabic'
            斯拉夫字母：'cyrillic'
            梵文字母：'devanagari'

    返回:
        str: 生成的 TXT 文件的路径。
    """

    full_dir_path = os.path.join(os.path.dirname(filepath), dir_path)
    if not os.path.exists(full_dir_path):
        os.makedirs(full_dir_path)
    ocr = PaddleOCR(use_angle_cls=True, lang=lang_code, use_gpu=USE_GPU, show_log=False)
    doc = fitz.open(filepath)
    txt_file_path = os.path.join(full_dir_path, f"{os.path.split(filepath)[-1]}.txt")

    # 利用 UUID 为每份文件的创建一个独特的临时文件名
    # 以免多线程运行时，临时文件之间发生干扰（错误覆盖）
    img_name = os.path.join(full_dir_path, f"{str(uuid.uuid4())}.png")
    if PRINT_LOG:
        print(f"start to process [ {filepath} ]\nthe temp image name is [ {img_name} ]")
    with open(txt_file_path, "w", encoding="utf-8") as fout:
        for i in range(doc.page_count):
            if PRINT_LOG:
                print(
                    f"start to process page < { str(i+1).ljust(3, ' ') } > of [[ { filepath} ]] "
                )
            page = doc[i]
            text = page.get_text("")
            fout.write(text)
            fout.write("\n")

            img_list = page.get_images()
            for img in img_list:
                pix = fitz.Pixmap(doc, img[0])
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(img_name)

                result = ocr.ocr(img_name)
                ocr_result = [i[1][0] for line in result for i in line]
                fout.write("\n".join(ocr_result))
    if os.path.exists(img_name):
        os.remove(img_name)
    return txt_file_path


if __name__ == "__main__":
    fname = "pdf/text_ver.pdf"
    txt_path = pdf_ocr_txt(fname)
    print(txt_path)
