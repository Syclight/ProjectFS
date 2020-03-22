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
* 新添加 clazz/RSA.py 用途是RAS文件加密
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
* 添加了modal文件夹，准备写用户模型，NPC模型，物理模型等