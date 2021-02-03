# _*_ coding: utf-8 _*_
import sys

sys.path.append('F:/Practice/PyCharm/PygameTest/venv/Lib/site-packages/')


def main():
    from source.core.const.Const import gl_WindowWidth, gl_WindowHeight, gl_nextLevelWindowWidth, \
        gl_nextLevelWindowHeight
    from gameApp import gameApp

    #  print(os.path.abspath(__file__))
    game = gameApp("FinalSound终曲", gl_nextLevelWindowWidth, gl_nextLevelWindowHeight, False, 0, 32)
    print('syclight_msg_gameapp_id: ' + str(game.getId()))
    game.MainLoop()


if __name__ == "__main__":
    main()
