# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pigai",                                         # 包的分发名称，使用字母、数字、_、-
    version="1.16",                                        # 版本号, 版本号规范：https://www.python.org/dev/peps/pep-0440/
    author="pigai",                                         # 作者名字
    author_email="1918118941@qq.com",                        # 作者邮箱
    description="Pigai Api",                            # 包的简介描述
    long_description=long_description,                      # 包的详细介绍(一般通过加载README.md)
    long_description_content_type="text/markdown",          # 和上条命令配合使用，声明加载的是markdown文件
    url="https://github.com/",                              # 项目开源地址，我这里写的是同性交友官网，大家可以写自己真实的开源网址
    packages=setuptools.find_packages(),                    # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
    dependency_links=['https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz#egg=en_core_web_sm'],
    install_requires=[
        'requests>=1.0',
        'spacy>=2.0.0',
        'pandas',
        'pygtrie',
        'seaborn',
        'numpy',
        'ipywidgets',
        'en_core_web_sm',
        'redis>=3.4.1',
        'elasticsearch'
    ]
)
