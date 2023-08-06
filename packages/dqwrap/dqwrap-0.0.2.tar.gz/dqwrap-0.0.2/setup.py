import os
from setuptools import setup, find_packages

# python setup.py check
# python setup.py sdist
# twine upload dist/dqwrap-*.tar.gz

path = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    with open(os.path.join(path, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name="dqwrap",
    version="0.0.2",
    keywords=["wrap", "5-layer" , "wrap layer"],
    description="wrap layer of 5-lay architecture",
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",

    author="daqian",
    author_email="daqian.zhang@g42.ai",
    url="http://assetik.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    platforms="any",

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'dqwrap=dqwrap:test'
    #     ]
    # },
    zip_safe=False

)
