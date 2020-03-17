# _*_ coding: utf-8 _*_


def main():
    from clazz.Const import gl_WindowWidth, gl_WindowHeight
    from gameApp import gameApp

    game = gameApp("FinalSound终曲", gl_WindowWidth, gl_WindowHeight, False, 0, 32)
    game.MainLoop()


if __name__ == "__main__":
    main()
