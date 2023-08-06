from distutils.core import setup

setup(
    name='mokuai',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',  #描述
    author='wangruihuan', # 作者
    author_email='371454659@qq.com',
    py_modules=['mokuai.ca1','mokuai.ca2'] # 要发布的模块
)