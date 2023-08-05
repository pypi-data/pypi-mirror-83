from distutils.core import setup

setup(
    name="PY_MK01", #对外我们模块的名字
    version="1.0", #版本号
    description="第一个对外发布的模块，测试", #描述
    author="DDHarper", #作者
    author_email="13602381744@163.com", #作者邮箱
    py_modules=["PY_MK01.demo01","PY_MK01.demo02"] #要发布的模块
)