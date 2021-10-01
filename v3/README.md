# 第三方依赖库及安装
```shell
# ffmpeg-python
pip install ffmpeg-python
# numpy
pip install numpy
# Pillow
pip install pillow
```

# ❇️ core.py
算法的一些关键函数实现，
包含**列采样**策略、**计算重合位置**、**预测和丢帧**策略。

### 1️⃣ sampling_yuv(array) 列采样函数
主要负责由一个图片矩阵中选取并处理几列的数据并返回。
```python
np.average(array[:, np.linspace(20, w / 4, 16, dtype='int')], axis=1)
np.average(array[:, np.linspace(w / 2, 5 * w / 8, 16, dtype='int')], axis=1)
np.average(array[:, np.linspace(6 * w / 8, 7 * w / 8, 16, dtype='int')], axis=1)
```
以第一行为例，表示从`x=20`, 到`x= w / 4`（w表示图片宽度） **等距**取16列，然后按行计算平均值，得到融合的一列数据。
最终选取的是16 * 3列，融合的3列。

### 2️⃣ better_offset(max, predict_y)
`max`表示最大的滑动距离，`predict_y`表示预测的滑动距离
例如，屏幕高度`1600px`，剪裁头尾各`300px`，还剩`1000px`，设定剪裁后最小的重合高度`300px`。
那么就需要分别比较滑动距离`0-700px`，max就是700。
假设预测值`predict_y`为300，那么该函数返回的是
`[300，301，299，302，298，303，297，...]`, 
目的在与快速找到结果（优先比较预测值附近的值），跳出循环。

### 3️⃣ predict_translation_y(column, column2, predict)
column, column2 是由采样函数sampling_yuv对图片采样返回的值，
predict是预测的滚动距离。
该函数按照 `better_offset()` 函数生成的列表依次比较，
若平均差小于设定的 `min_avg_diff` 则准备跳出循环。
跳出循环前，再比较最后10次（目的在与让拼接位置更准确一点）。

### 4️⃣ predict(list, idea_offset)
该函数实现了预测和丢帧的策略。
list 是一个之前几次计算结果的列表，
每次的计算结果由一个元组表示，例如(2, 30, 0.1111) 表示第2帧，滚动距离30px，
平均绝对差异值为0.1111。
idea_offset 表示期望的滚动距离，假设我期望的滚动距离是300px, 而根据之前的结果，
每帧滚动了90px, 那么可以计算到，距离达到期望的滚动距离还有3.3帧，
那就可以丢2帧，假设滚动是线性的（这几帧的滚动距离也是每帧90px），
那么预测的滚动距离就是270px。


# ▶️ splicing.py
调用core.py提供的关键函数，进行实际拼接。
可分为如下3部分：
1. FFmpeg视频读帧
2. 调用 core.py 计算重合位置
3. 拼接长图
