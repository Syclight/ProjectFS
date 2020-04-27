class CollidedProbe:
    @staticmethod
    def execute(act, pas, unitTime):
        if not act.hasCollidedProbe:
            return
        if not pas.hasCollidedProbe:
            return

        actV = act.vel.copy()
        pasV = pas.vel.copy()

        M = act.mass + pas.mass
        actV_ = (actV.mul(act.mass - pas.mass) + pasV.mul(2 * pas.mass)).dev(M)
        pasV_ = (pasV.mul(pas.mass - act.mass) + actV.mul(2 * act.mass)).dev(M)

        actAveV = (actV + actV_).mul(0.5)
        pasAveV = (pasV + pasV_).mul(0.5)

        actD = actAveV.mul(1)
        pasD = pasAveV.mul(1)

        actD_inv = actD.invert()
        pasD_inv = pasD.invert()

        actF_ = actD_inv.mul((0.5 * act.mass * (actV_.dot(actV_) - actV.dot(actV))))
        pasF_ = pasD_inv.mul((0.5 * pas.mass * (pasV_.dot(pasV_) - pasV.dot(pasV))))

        if pas.collideArea.bottom() > act.collideArea.top():
            pas.collideArea.y = act.collideArea.top() - pas.collideArea.h
        if pas.collideArea.right() < act.collideArea.left():
            pas.collideArea.x = act.collideArea.left() - pas.collideArea.w

        act.applyForce(actF_)
        pas.applyForce(pasF_)

        # if act.vel.y < actV.y:
        #     act.vel.y = 0
        # if pas.vel.y < pasV.y:
        #     pas.vel.y = 0
