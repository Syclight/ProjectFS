from source.view.baseClazz.Sprite import Sprite


class CursorSprite(Sprite):
    def __init__(self, *args, colorKey=(0, 0, 0)):
        super(CursorSprite, self).__init__(image='F:/Practice/PyCharm/PygameTest/source/view/origin/res/cursor.bmp')
        self.zIndex = 100
        self.image.set_colorkey(colorKey)
        self.visual = False

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
