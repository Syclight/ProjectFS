# _*_ coding: utf-8 _*_
# import pygame
# import gc
#
# from clazz.Scene import *
# from sys import exit
# from clazz.Const import *
#
#
# def _gcRelease(e):
#     del e
#     gc.collect()
#
#
# # 全局变量
# g_SceneNum = 0
#
# # 初始化pygame,这里不需要初始化也可以？
# pygame.init()
# # 创建窗口
# window = pygame.display.set_mode((gl_WindowWidth, gl_WindowHeight), 0, 32)
# # 设置标题
# pygame.display.set_caption("FinalSound终曲")
#
# # 音频系统初始化
# pygame.mixer.init()
#
# # 载入初始场景
# scene = LogoScene(window)
# print('FinalSound终曲 pygame重置版\n-----控制台-----')
#
# # 游戏主循环
# while True:
#     # 事件处理
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             _gcRelease(scene)
#             pygame.mixer.quit()
#             pygame.quit()
#             exit()
#         elif event.type == pygame.MOUSEMOTION:
#             scene.doMouseMotion(event.pos, event.rel, event.buttons)
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             scene.doMouseButtonDownEvent(event.pos, event.button)
#         elif event.type == pygame.MOUSEBUTTONUP:
#             scene.doMouseButtonUpEvent(event.pos, event.button)
#     # 清屏
#     window.fill((0, 0, 0))
#
#     if scene.isEnd:
#         g_SceneNum = scene.nextSceneNum
#         if g_SceneNum == 1:
#             _gcRelease(scene)
#             scene = TitleScene(window)
#         elif g_SceneNum == 10:
#             _gcRelease(scene)
#             scene = NewGame_First_StoryScene(window)
#         elif g_SceneNum == 30:
#             _gcRelease(scene)
#             scene = Option_Scene(window)
#         elif g_SceneNum == 301:
#             _gcRelease(scene)
#             scene = Option_Scene(window, True)
#     # 画屏幕
#     scene.draw()
#
#     # 刷新画面
#     pygame.display.update()
from clazz.Const import gl_WindowWidth, gl_WindowHeight
from gameApp import gameApp

game = gameApp("FinalSound终曲", gl_WindowWidth, gl_WindowHeight, False, 0, 32)
game.MainLoop()
