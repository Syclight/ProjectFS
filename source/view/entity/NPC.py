from source.view.baseClazz.Actor import Actor
from source.model.User import User


class NPC(Actor, User):
    def __init__(self, texture, area):
        Actor.__init__(self, texture, area)
        User.__init__(self)
