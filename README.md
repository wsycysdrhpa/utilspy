## utilspy

### 功能说明
**python项目的通用工具库**

推荐使用示例(默认windows环境, linux下类似)：
1. 通过git clone下载utilspy包，下载位置H:\Code\Tools\Python\tools\，tools同级文件夹中需要有`__init__.py`文件，这样才能import:
  git clone https://github.com/wsycysdrhpa/utilspy.git；
2. 在python的site-package目录下创建一个utils.pth文件；
3. 在utils.pth文件中写入tools所在的文件夹路径，例：H:\Code\Tools\Python\

### 测试
```
>>> from tools.utilspy.time.time_helper import TimeHelper
>>> print TimeHelper.now()
```

备注：
放置在tools下是为了以后多机部署时候更加方便，不需要每台机器都下载工具，
只需要在工程中新建tools文件夹(包含`__init__.py`)，并将utilspy拷贝过来就可以使用，且不需要改动代码
