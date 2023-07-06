# 〇、环境配置

1. 安装 `PaddlePaddle`

   根据百度官方的快速安装，直接复制对应的安装命令；如果有 CUDA 环境，在 OCR 时，应该能快很多。

   > [https://www.paddlepaddle.org.cn/install/quick](https://www.paddlepaddle.org.cn/install/quick)

2. 安装 `PaddleOCR`

   `pip install paddleocr`

# 一、主要思路

- 读取 PDF 文件
- 遍历 PDF 中的每一页
  - 首先，提取出一页中的 文字，并保存到 txt 文件
  - 其次，提取出一页中的 图像，将图像保存为临时文件
    - 对图像进行 OCR， 将得到的文字保存到 txt 文件
- 删除临时文件（之所以在最后删除，因为之前的过程中，后一张临时图片会覆盖前一张临时图片）

# 二、关于如何集成到原有工作流程中的想法

把处理 PDF 文件的问题转换为处理 txt 文件的问题。

当接收到一个 PDF 文件后，通过这的函数，将 PDF 中的文字提取并存储到 txt 文件当中，使用 txt 的 loader 进行加载。
