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