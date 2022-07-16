# screenshot-splicing

Python滚动截长图的简单算法实现，由视频读帧计算滚动距离并拼接长图。

支持上下双向滚动，支持预测和跳帧，核心代码 < 200行

## 安装依赖
```shell
# ffmpeg-python, numpy, pillow

pip install ffmpeg-python
pip install numpy
pip install pillow

# ffmpeg (https://ffmpeg.org/)

apt install ffmpeg
```

## 用法
```sh
./splicing ../examples/a.mp4
```

## ❇️ core
算法的一些主要函数实现

### 1️⃣ col_sampling(img_array: np.ndarray, cols_group=None) 
列采样函数, 由一个图片矩阵中选取并处理几列的数据并返回。

`img_array`: 灰度图片（矩阵）

`cols_group`: 自定义采样策略， 例如：
- cols_group=[[1]] - 只取第1列
- cols_group=[[1,5],[6,9]] - 分别取第1，5列和第6，9列的平均值



### 2️⃣ predict_offset(max: int, p: int)
根据预测值生成一个偏移值列表

`max`: 最大的滚动距离绝对值

`p`: 预测的滚动距离（offset）

例如滚动范围是`(-100, 100)`（`max=100`）, 预测的滚动距离是`50`(`p=50`)。

则返回的列表是`[50, 51, 49, 52, 48, ...]`

也就是由预测值开始，向预测值左右依次比较


### 3️⃣ diff_overlap(cols: np.ndarray, col2: np.ndarray, predict=0, approx_diff=0.2, min_overlap=220)

`cols`, `cols2`:  是由采样函数`col_sampling`对图片采样结果

`predict`: 预测的滚动距离

`approx_diff`: 可以接受的差异值，比较差异时小于该值返回

`min_overlap`: 可接受的最小重叠高度（px）


若平均差小于设定的 `approx_diff` 则准备跳出循环,跳出循环前，再比较最后10次（目的在与让拼接位置更准确一点）。


### 4️⃣ predict(history: list, idea_offset)
该函数实现了预测和丢帧的策略。
list 是一个之前几次计算结果的列表，
每次的计算结果由一个元组表示，例如(2, 30, 0.1111) 表示第2帧，滚动距离30px，
平均绝对差异值为0.1111。
idea_offset 表示期望的滚动距离，假设我期望的滚动距离是300px, 而根据之前的结果，
每帧滚动了90px, 那么可以计算到，距离达到期望的滚动距离还有3.3帧，
那就可以丢2帧，假设滚动是线性的（这几帧的滚动距离也是每帧90px），
那么预测的滚动距离就是270px。


### calc_overlaps


### splice

# ▶️ splicing.py
调用core.py提供的关键函数，进行实际拼接。
可分为如下3部分：
1. FFmpeg视频读帧
2. 调用 core.py 计算重合位置
3. 拼接长图
