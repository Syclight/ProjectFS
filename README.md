# ProjectFS
FS的python重置版，只不过没有资源

### 2020.3.17 Asheor
* 修改了main.py 将注释删去，添加了入口函数
* 修改了gameApp.py中循环的判断条件
* 添加了example文件夹，用途是练习用的例子

### 2020.3.18 Asheor
* 主要更新了IOEvent.py中的IOEvent3
> IOEvent3 更新：
>>* Scene 可以自动识别可交互Element和固定Element
>>* 现在支持去除已绑定的事件
>>* 加入事件的ID标识，内部生成策略采用hash函数
* 修改了与IOEvent3相关的代码
> Scene.py 和 Element.py

### 2020.3.19 Asheor
* ToolsFuc.py 添加了一种随机数发生器，算法为梅森旋转法(Mersenne Twister MT)
* Scene.py 去掉了Scene的无效导入
* IOEvent.py 修改了IOevent3在处理键盘事件的细节

### 2020.3.20 Asheor
* Scene.py 每个场景的初始化方法均加入了参数列表，同时将CG播放场景和序章场景分割独立。
> 原因：
> 用以前的方法，在序章场景开始的时候，即便没有播放CG，程序也会提前运行FFmpeg的进程。
> 将CG播放独立成一个场景，使得FFmpeg的进程在播放CG时开启，在播放完毕后销毁
* Const.py 修正了一处英语单词的错误拼写，添加了新的CG场景的场景号 SCENENUM_GAME_STARTCG
* 修改了CG资源的名称

### 2020.3.21 Asheor
* 新添加 clazz/RSA.py 用途是RSA文件加密
* 新添加 RecordFile.py 用途是生成游戏的记录文件,文件格式.rf
* 在 Element.py 中添加了 Element 接口，使所有的Element实现该接口
* 在 Const.py 中添加了rf文件相关的常量和NUM_DICT系列映射关系
* 在 ToolsFuc.py 中添加了根据Const映射转换的函数

### 2020.3.22 Asheor
* RecordFile.py 更新了游戏记录文件的文件结构
* Scene.py 添加了继续游戏选项的场景(试行版)
* Element.py 添加了一种继续游戏场景中的元素
* RSA.py 优化程序对RSA函数的调用
* 添加了一个测试：example/RecordFileAndRSATest.py
* 添加了model文件夹，准备写用户模型，NPC模型，物理模型等

### 2020.3.24 Asheor
* Scene.py 将Scene由接口模式，转变成继承模式。同时将一些场景的事件触发机制做了调整。
* IOEvent.py 向IOEvent3中添加了一种可处理的事件：鼠标在元素中移动事件
* Config.py 调整了Config读取配置的方式，现在不需要再各场景中重新建立对象
* gameApp.py 修改了在程序没有加载完成时，窗口标题显示为"pygame window"的情况
* ToolsFuc.py 添加了归并排序
* 关于Element，暂时决定成接口实现的模式，就这样吧

### 2020.3.25 Asheor
* gameApp.py 加入了帧率的设定，最大120帧，最小30帧，方便对游戏渲染过程的修改
* Scene.py 重写了序章的场景，使其可以运行在相应帧率的配置下, 同时重新编排了场景的演出效果
* 在 Const.py 与 Config.py 中加入了帧率相关设定，同时进一步改进了场景对Config的读取方式

### 2020.3.26 Asheor
* IOEvent.py, IOEvent3重大更新！
> * 现在ioEvent3Enum 不继承enum类，因为python的enum类不太好用
> * 修改了事件ID标识的处理方法,不再使用hash
> * 完善了对键盘事件的支持
> * 添加了一个关于IOEven3的测试例子，在example文件夹下
* 添加了gameElementsAndScene文件夹，用来存放与游戏场景有关的类 Sprite.py
* 在框架中添加了对精灵的支持，精灵也可以使用IOEvent3进行交互
* ToolsFuc.py 添加了pygame按键到ioEvent3按键的映射函数，还有一些其它的
* gameApp.py 添加了长按事件的支持
* model文件夹下添加了一个Shape.py
* Scene.py, Element.py 修改了Scene基类和Elements中的一些细节
* 今天决定将这个游戏的框架命名为Syclight GameFramework with python,为Syclight的一份子

### 2020.3.28 Asheor
* 添加了SpriteGroup，主要是对pygame中的改造，可以实现组内碰撞检测，同时防止一些莫名其妙bug的产生
> 碰撞检测数据结构：四叉树
* 对QuadTree.py做了更加规范化的调整
* 对Shape.py中的类做了升级优化
* 添加了三例测试
> ShapeTest.py 测试Shape.py,
> 精灵动画播放测试：testSpriteScene.py,
> 碰撞测试: testSpriteScene.py
* 其它的做了一些修改

### 2020.3.29
* 更新了目录结构  
目录名称|子文件夹|备注
-|-|-
source|(all)|包含全部的源文件
config|(null)|主要是App的配置文件 AppConfig
const|(null)|常量
controller|assembly,dataStructure|程序要用到的组件，数据结构等
examples|(null)|测试用例
model|(null)|模型
util|(null)|工具包
view|bassClass,element,entity,scene|游戏视图，baseClass中有一游戏中用到的基类
* 继续完善了Shape.py
* 新建立Actor.py，Actor为游戏中出现的所有物体
