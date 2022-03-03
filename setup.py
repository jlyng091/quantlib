# run via pip install -e .
# or pip install --editable .

import setuptools

setuptools.setup(
    name='quantlib',
    version='0.1',
    description='quantlib by jln',
    url='0',
    author='Justin L. Ng',
    install_requires=['numpy', 'pandas', 'talib; python_version=="0.4.19"'],
    author_email='',
    packages=setuptools.find_packages(),
    zip_safe=False
)
