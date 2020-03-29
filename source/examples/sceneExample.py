from source.view.scene.Scenes import Scene


class exampleScene(Scene):
    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.isEnd = False
        self.nextSceneNum = 0

        print('第一个example场景创建完成')

    def draw(self):
        print('这是第一个example场景的draw')

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        print('这是第一个example场景的处理鼠标移动事件')
        print('鼠标位置：', MousePos)
        print('鼠标移动量：', MouseRel)
        print('鼠标的按键状态：', Buttons)

    def doMouseButtonDownEvent(self, MousePos, Button):
        print('这是第一个example场景的处理鼠标点击事件')
        print('鼠标位置：', MousePos)
        print('鼠标的按键：', Button)

    def doMouseButtonUpEvent(self, MousePos, Button):
        print('这是第一个example场景的处理鼠标松开事件')
        print('鼠标位置：', MousePos)
        print('鼠标的按键：', Button)


class exampleScene2(Scene):
    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.isEnd = False
        self.nextSceneNum = None
        print('第二个example场景创建完成')

    def draw(self):
        print('这是第二个example场景的draw')

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        print('这是第二个example场景的处理鼠标移动事件')
        print('鼠标位置：', MousePos)
        print('鼠标移动量：', MouseRel)
        print('鼠标的按键状态：', Buttons)

    def doMouseButtonDownEvent(self, MousePos, Button):
        print('这是第二个example场景的处理鼠标点击事件')
        print('鼠标位置：', MousePos)
        print('鼠标的按键：', Button)

    def doMouseButtonUpEvent(self, MousePos, Button):
        print('这是第二个example场景的处理鼠标松开事件')
        print('鼠标位置：', MousePos)
        print('鼠标的按键：', Button)
