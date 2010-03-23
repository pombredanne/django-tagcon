import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-tagcon',
    version='0.1alpha1',
    description="A template tag constructor library for Django.",
    long_description=read('README.rst'),
    author='Tom X. Tobin',
    author_email='tomxtobin@tomxtobin.com',
    license='MIT',
    url='http://github.com/tomxtobin/django-tagcon',
    packages=['tagcon'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
