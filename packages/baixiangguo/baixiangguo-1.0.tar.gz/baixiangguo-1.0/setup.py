#encoding=utf-8
from distutils.core import setup

setup(
    name='baixiangguo',#对外我们模块的名字
    version='1.0', #版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',#描述
    author='heyuting',
    author_email='2356854359@qq.com',
    py_modules=['baixiangguo.demo1','baixiangguo.demo2'] #要发布的模块；
)