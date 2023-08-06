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
    version='0.0.3',
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
    keywords='api workwechat',
    packages=["wwr_api"],
)
