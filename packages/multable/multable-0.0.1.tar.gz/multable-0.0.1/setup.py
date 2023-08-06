import setuptools

def jiujiu():
    for i in range(1, 10):
        for j in range(1, i+1):
            print('{}x{}={}\t'.format(j, i, i*j), end='')
        print()
 




setuptools.setup(
    name="multable", # Replace with your own username
    version="0.0.1",
    author="李厚奇",
    author_email="884359533@qq.com",
    description="调用此方法可打印9*9乘法表",
    long_description='调用此方法可以打印9*9乘法表',
    long_description_content_type="text/markdown",
    url="https://github.com/tanxinyue/multable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)