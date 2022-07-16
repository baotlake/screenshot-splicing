# OpenCV Stitcher

使用openCV Stitcher class进行拼接

## 用法
```shell
# scans
./scans.py ../img/1/a.png ../img/1/b.png

# stitcher
./stitcher.py ../img/1/a.png ../img/1/b.png

```

### ./stitching.py
该文件 clone 自[website-screenshot-stitching](!https://github.com/Ahtuz/website-screenshot-stitching)

`./stitcher.py` 对 `./stitching.py` 做了少许改动，以便于命令行更灵活的使用。

### ./scans.py
使用OpenCV Stitcher 的 SCANS 模式（更适合拼接仿射变换的图）


