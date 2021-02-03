from lxml import etree


class HtmlOperator:
    def __init__(self):
        pass

    @staticmethod
    def readFromFilePath(path, encoding='utf-8'):
        f = open(path, 'r', encoding=encoding)  # 读取文件
        f = f.read()  # 把文件内容转化为字符串
        html = etree.HTML(f)  # 把字符串转化为可处理的格式
        return html

    @staticmethod
    def readText(Text):
        return etree.HTML(Text)  # 把字符串转化为可处理的格式

h = HtmlOperator()
s = h.readText('<a href="javascript:void(0);" id="green_channel_digg" ">好文要顶</a>')
print(s)