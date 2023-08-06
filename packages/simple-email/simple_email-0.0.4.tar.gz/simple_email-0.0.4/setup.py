# import setuptools
#
# with open("README.md", "rb") as fh:
#     long_description = fh.read()
# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
#     version="0.0.1",
#     author="ken",
#     author_email="596600794@qq.com",
#     description="开箱即用的邮件发送包",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/fanfan531/simple-email",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )



#from distutils.core import setup
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

VERSION = '0.0.4'

tests_require = []

install_requires = []

setup(name='simple_email', # 模块名称
      url="https://github.com/fanfan531/simple-email",
      author="ken",  # Pypi用户名称
      author_email='596600794@qq.com',  # Pypi用户的邮箱
      description='开箱即用的邮件发送包',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',  # 开源许可证类型
      classifiers=[
          # "Operating System :: OS Independent",
          # 'Topic :: Software Development',
          # 'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},
      entry_points={ 'nose.plugins': [] },
      packages=find_packages(),
)