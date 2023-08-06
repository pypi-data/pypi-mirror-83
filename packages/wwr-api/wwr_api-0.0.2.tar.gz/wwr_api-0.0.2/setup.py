import os

import requests
from setuptools import setup


def md_to_rst(from_file, to_file):
    res = requests.post(url='http://c.docverter.com/convert',
                        data={'to': 'rst', 'from': 'markdown'},
                        files={'input_files[]': open(from_file, 'rb')})
    if res.ok:
        with open(to_file, "wb") as f:
            f.write(res.content)


md_to_rst("README.md", "README.rst")

setup(
    name='wwr_api',
    version='0.0.2',
    description='WorkWechat Robot APIs',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    python_requires='>=3.4',
    url='https://github.com/Thoxvi/WorkWechat-Robot-API',
    author='Thoxvi',
    author_email='A@Thoxvi.com',
    install_requires=[
        "requests"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='api workwechat',
    packages=["wwr_api"],
)
