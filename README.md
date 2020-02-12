## utilspy

### 功能说明
**python项目的通用工具库**

推荐使用示例(默认windows环境, linux下类似)：
1. 通过git clone下载utilspy包，下载位置如：H:\Code\Tools\Python\,
git clone https://github.com/wsycysdrhpa/utilspy.git;
2. 在python的site-package目录下创建一个utils.pth文件；
3. 在utils.pth文件中写入utilspy所在的文件夹路径，例：H:\Code\Tools\Python\

### 测试
```
>>> from utilspy.time.time_helper import TimeHelper
>>> print TimeHelper.now()
```

备注：
多机部署时直接拷贝到工程下更加方便，不需要每台机器都下载工具


python3版本支持
regularization/*
dict/*
environment/*
log/*
text/*
time/*


python2版本支持
其他
