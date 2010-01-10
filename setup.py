import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-tagcon',
    version='0.1alpha1',
    description="A template tag constructor library for Django.",
    long_description=read('README.rst'),
    author='Tom Tobin',
    author_email='korpios@korpios.com',
    license='MIT',
    url='http://github.com/korpios/django-tagcon',
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
