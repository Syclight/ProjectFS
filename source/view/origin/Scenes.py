from source.view.baseClazz.Scene import Scene

g_resPath = 'res/'

class OriginLogo(Scene):
    def __init__(self, *args):
        super(OriginLogo, self).__init__(*args)
        self.resPath = {'bg':g_resPath + 'bg.jpg'}

    def setup(self):
        