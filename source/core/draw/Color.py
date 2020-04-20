from source.core.math.Vector import vec3


# class color:
#     """颜色类"""
#     def __init__(self, r, g, b, a=255):
#         # self.valRGB = 0xFF000000 | ((round(r * a) & 0xFF) << 16) | ((round(g * a) & 0xFF) << 8) | round(b * a) & 0xFF
#         self.val = ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | b & 0xFF
#
#     def aryRGBA(self):
#         return (self.val >> 16) & 0xff, (self.val >> 8) & 0xff, self.val & 0xff, (self.val >> 24) & 0xff
#
#     def aryRGB(self):
#         return (self.val >> 16) & 0xff, (self.val >> 8) & 0xff, self.val & 0xff
#
#     def getR(self):
#         return (self.val >> 16) & 0xff
#
#     def getG(self):
#         return (self.val >> 8) & 0xff
#
#     def getB(self):
#         return self.val & 0xff
#
#     def getAlpha(self):
#         return (self.val >> 24) & 0xff
#
#     def blendFactor(self):
#         return round(self.getAlpha() / 255, 1)
#
#     @staticmethod
#     def mix__(bottom, top):
#         bf_a, tf_a = bottom.blendFactor(), top.blendFactor()
#         # br = bottom aryRGBA

class color:
    """颜色类"""

    def __init__(self, *args):
        self.r, self.g, self.b, self.a = 0, 0, 0, 1
        if len(args) == 1:
            # Gray = (R * 38 + G * 75 + B * 15) >> 7
            gray = args[0]
            self.__init__(255 * gray, 255 * gray, 255 * gray)
        if len(args) == 2:
            gray = args[0]
            self.__init__(255 * gray, 255 * gray, 255 * gray, args[1])
        if len(args) == 3:
            self.r, self.g, self.b = round(args[0]), round(args[1]), round(args[2])
        if len(args) == 4:
            self.r, self.g, self.b, self.a = round(args[0]), round(args[1]), round(args[2]), args[3]

    def __str__(self):
        return '<color::{}({}, {}, {}, {})>'.format(self.__class__.__name__, self.r, self.g, self.b, self.a)

    @staticmethod
    def fromVec3(v, a=1):
        return color(v.x, v.y, v.z, a)

    @staticmethod
    def mix_(top, bottom):
        r1, g1, b1, a1 = top.r, top.g, top.b, top.a
        r2, g2, b2, a2 = bottom.r, bottom.g, bottom.b, bottom.a

        r3 = r1 * a1 + r2 * a2 * (1 - a1)
        g3 = g1 * a1 + g2 * a2 * (1 - a1)
        b3 = b1 * a1 + b2 * a2 * (1 - a1)
        a3 = 1 - (1 - a1) * (1 - a2)

        return color(r3, g3, b3, a3)

    def aryRGBA(self):
        return self.r, self.g, self.b, self.a

    def aryRGB(self):
        return round(self.r * self.a), round(self.g * self.a), round(self.b * self.a)

    def valRGBA(self):
        a_ = round(255 * self.a)
        return ((a_ & 0xFF) << 24) | ((self.r & 0xFF) << 16) | ((self.g & 0xFF) << 8) | self.b & 0xFF

    def valRGB(self):
        rgb = self.aryRGB()
        return 0xFF000000 | ((rgb[0] & 0xFF) << 16) | ((rgb[1] & 0xFF) << 8) | rgb[2] & 0xFF

    def vector3(self):
        rgb = self.aryRGB()
        vec3(rgb[0], rgb[1], rgb[2])

# red = color(255, 0, 0, 255)
# blue = color(0, 0, 255, 180)
# mix = color.mix_(blue, red)
# print(hex(mix.val))
# print(hex(blue.val_), hex(red.val_), hex(mix.val_))

# red = color(255, 10, 0, 105)
#
# print(red.aryRGBA())
