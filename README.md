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

### 2020.3.29  Asheor -Code:Reborn
* 更新了目录结构  
目录名称|子文件夹|备注  
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

### 2020.3.30 Asheor
* 添加controller.assembly.XmlOperator.py用于操作XML文件
* 添加PhysicalBody.py用于物理组件，同时还添加了PhysicsSystem
* 添加chapter1-1.py准备进入第一章节游戏的编写
* 将vec2等添加到util.Math2d.py中

### 2020.4.4 Asheor
* 主要更新2d物理方面的支持：力，与碰撞反馈
* PhysicsSystem 更名为PhysicalScene
* 与物理支持有关的文件：
> 1.controller/assembly/CollidedProbe.py 该文件为碰撞处理探针，处理碰撞之后各个物理体的状态，由physicalScene调用  
> 2.controller/assembly/PhysicalBody.py 该文件为主要的物理处理机，包含physicalBody与PhysicalScene  
> 3.util/Math2D.py 添加了许多2d向量的新计算方式，方便进行物理运算  
> 4.controller/assembly/Shape.py 为方便物理运算添加了一些特性
* 在examples下可以找到对应的测试场景，修改AppConfig.py以测试
* 优化了gameApp.py， 现在在创建场景时要传入时间参数(这个时间一般用pygame.time.get_ticks()获得)

### 2020.4.7 Asheor
* 重大更新！本次主要添加了A*寻路算法
* A-star.py 主要包含A*寻路算法的各种细节
* 添加了MathUtil.py提供一些与数学相关的函数
* 添加了一个测试AstartTest.py同样在AppConfig.py中配置后即可使用
* 轻微修改了CollidedProbe.py与PhysicalBody.py

### 2020.4.8 Asheor
* 修改了A-start.py中的一些细节，使寻路在实际应用中更加方便

### 2020.4.13 Asheor
* 新增的Painter.py可以画出Shape中的形状
* 新增了一个测试 TestPainter.py 用于测试绘制Shape的效果
* 新增了MathConst.py 数学常量
* Math2d.py 新增了行列式计算
* A-start.py 更名为A_start.py，并做了少量修改。
* Shape.py 新增了Line与Ellipse

### 2020.4.14 Asheor
* 对MathUtil.py,Painter.py,ToolsFuc.py,A_star.py进行了细节上的修改
* 修改了测试TestPainter.py与testSpriteScene.py
* 添加了RTS_Test.py测试A*和Actor结合，模拟RTS的寻路系统

### 2020.4.15 Asheor
* 将A*寻路结合到场景中，详见RTS_Test.py
* 修复了Painter画直线时起点有时会错误的bug
* 修复了Math2d.py中向量求夹角时cos值未定义边界而错误的问题，添加了求正方向的方法
* MathUtil.py与MathCost.py中添加了插值函数相关的方法，现在支持：
> 线性插值，三角插值，立方差值(三次插值)，Hermite插值
* 添加SGFpyException.py,是框架中所有异常的基类
* A_star.py现在支持插入一个障碍物域与删除障碍物域,并添加了位置错误异常

### 2020.4.16 Asheor
* 柏林噪声终于在框架中实现，参考了p5.js，core.math.Noise
* 重新将代码目录分配，新建了core，主要存放框架的核心支撑代码
* 数学有管的在core.math下
* 修改了Scene基类，现在在初始化时，可以直接传参*args
* 新增了Map.py, noiseTest.py, Random.py

### 2020.4.17 Asheor
* 添加了非常有趣的测试场景，someFunTestScene.py
> 画板，波图像，绘制球体草稿与链条。用做框架Scene的教学，代码逻辑参考了p5.js的范例
* 修改了若干bug
* 新调整了gameApp的逻辑和新增Scene内置对象
* 我开通了LOFTER主页: https://syclightframework.lofter.com 欢迎访问

### 2020.4.20 Asheor
* 修改了若干代码
* 主要是研究canvas的实现，发现需要硬件加速来完成，不然像素计算太慢了。
* 添加了Matrix.py 用于矩阵的计算。
* 进一步修改scene的基类的结构，使其更加合理。

### 2020.4.27 Asheor
* 修改了gameApp的结构，scene的结构
> 带有super前缀的方法，不能重写。  
> 添加了许多内置对象与变量，方便编程
* 添加了渲染器类，用于分层渲染，类似于html中标签的z-index属性
* 添加了有趣的例子，用于学习使用该框架编程

### 2020.4.30 Asheor
* 添加了Component目录，里面是组件
> Constructor.py 生成器  
> Transform.py 变换组件