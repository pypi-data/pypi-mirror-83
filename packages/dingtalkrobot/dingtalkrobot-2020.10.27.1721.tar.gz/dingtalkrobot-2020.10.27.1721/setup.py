from distutils.core import setup
from setuptools import find_packages

setup(name='dingtalkrobot',  # 包名
      version='2020.10.27.1721',  # 版本号
      description='一个钉钉自定义机器人消息的Python封装库,可发送文本和文件',
      long_description='',
      author='mystic',
      author_email='799****65@qq.com',
      url='',
      license='',
      install_requires=["requests"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('dingtalk'),  # 必填，就是包的代码主目录
      package_dir={'': 'dingtalk'},  # 必填
      include_package_data=True,
      )
