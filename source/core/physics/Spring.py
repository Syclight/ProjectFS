from source.core.math.Vector import vec2


class Spring:
    # K_normalSpring = 7.9  # 普通弹簧
    # K_stainlessSteelSpring = 7.2  # 不锈钢丝
    # K_siliconBronzeSpring = 4.1  # 硅青铜线

    def __init__(self, beginMass, endMass, length, K, frictionConst):
        self.beginMass = beginMass
        self.endMass = endMass
        self.length = length
        self.K = K
        self.frictionConst = frictionConst

    def execute(self, fixed=0):
        variable = self.beginMass.local - self.endMass.local
        var_len = variable.len()
        force = vec2()
        if var_len != 0:
            force += variable.dev(var_len).mul((var_len - self.length) * (-self.K))
        force += (self.beginMass.velocity - self.endMass.velocity).negate().mul(self.frictionConst)
        if not fixed:
            self.beginMass.applyForce(force)
            self.beginMass.update()

        self.endMass.applyForce(force.negate())
        self.endMass.update()
