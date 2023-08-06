import collections
import setuptools

setuptools.setup(
    name='horkos',
    version='0.0.10',
    description=(
        'A library for validating data at the edges of big data systems.'
    ),
    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',
    url='https://gitlab.com/kjschiroo/horkos',

    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['horkos=horkos.cmdline:main'],
    },
    project_urls=collections.OrderedDict(
        (
            ('Documentation', 'https://horkos.readthedocs.io/'),
            ('Code', 'https://gitlab.com/kjschiroo/horkos'),
            ('Issues', 'https://gitlab.com/kjschiroo/horkos/-/issues'),
        )
    ),
    install_requires=['pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
