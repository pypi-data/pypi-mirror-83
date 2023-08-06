import setuptools

setuptools.setup(
    name='horkos',
    version='0.0.9',
    description='A package for validating incoming data.',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',
    url='https://gitlab.com/kjschiroo/horkos',

    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['horkos=horkos.cmdline:main'],
    },
    install_requires=['pyyaml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
