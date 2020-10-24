import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pycmarkgfm',
    version='1.0.1',
    description="Bindings to GitHub's Flavored Markdown (cmark-gfm), with enhanced support for task lists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zopieux/pycmarkgfm',
    author='Alexandre Macabies',
    author_email='web@zopieux.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    cffi_modules=["pycmarkgfm/build_cmark.py:ffibuilder"],
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
    project_urls={
        'Bug Reports': 'https://github.com/zopieux/pycmarkgfm/issues',
        'Source': 'https://github.com/zopieux/pycmarkgfm',
    },
    zip_safe=False,
    include_package_data=True,
)
