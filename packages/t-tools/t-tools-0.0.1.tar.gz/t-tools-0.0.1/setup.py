from setuptools import setup, find_packages

with open('readme.rst') as f:
    readme = f.read()

setup(
    name="t-tools",
    packages=find_packages(),
    version='0.0.1',
    description="t-tools",
    long_description=readme,
    author="wanghaifei",
    author_email='779598160@qq.com',
    url="https://github.com/coco369/tools",
    download_url='https://github.com/coco369/tools',
    keywords=['command', 'line', 'tool'],
    classifiers=[],
    entry_points={
        'console_scripts': [

        ]
    },
    install_requires=[
        'python3.7.6',
    ]
)
