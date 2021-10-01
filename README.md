# Screenshot Splicing

用Python拼接屏幕截图, 由录屏视频取帧拼接屏幕长截图

v1，v2, v3 是3个不同实现程度的版本，各自独立完整，没有互相依赖。
直接看最新版 [v3](./v3/README.md) 即可。

## v3 预测+丢帧
[v3 - 文档](./v3/README.md)
#### 用法
```shell
cd v3

./splicing.py ../video/a.mp4

# 或者
python3 ./splicing.py ../video/a.mp4

```

## v2 由录屏视频拼接

[v2 - 文档](./v2/README.md)

`./splicing ./video/a.mov`

拼接好的长图位于`./tmp/`目录下。

## v1 拼接多张图片
[v1 - 文档](./v1/README.md)

`cd ./v1`
`./splicing.py ./img/1/a.png ./img/1/b.png`
`./splicing.py ./img/1/*`


