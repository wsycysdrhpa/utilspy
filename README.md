## yzs_utils

### 功能说明
yzs_utils为python项目的通用工具库

### 使用方法

1. 通过git下载python-utils包，解压到某一文件夹；（建议通过git clone）
2. 在python的site-package目录下创建一个utils.pth文件；
3. 在utils.pth文件中写入python-utils的文件夹路径，例：E:\work\utils\python-utils\yzs_utils
4. 测试：

```
>>> import yzs_utils
>>> from yzs_utils.time.time_helper import TimeHelper
>>> print TimeHelper.now()
2016-12-24 03:26:15
>>> 
```
