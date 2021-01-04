from source.view.baseClazz.Element import Element


class Widget(Element):
    def __init__(self, area):
        super(Widget, self).__init__(area)


class ComboBox(Widget):
    def __init__(self, area, keyValDict):
        super(Widget, self).__init__(area)
        self.__content = keyValDict
        self.__currentSelect = None
        self.__defaultText = ''
        self.__defaultButt = ''

    def setCaption(self, text):
        self.__defaultText = text

