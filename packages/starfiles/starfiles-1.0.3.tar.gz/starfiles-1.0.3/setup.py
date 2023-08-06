from setuptools import setup

with open('README.md', 'r') as fh:
   long_description = fh.read()
setup(
    name='starfiles',
    version='1.0.3',    
    description='Simplify starfiles, if it was not simple already.',
    url='https://github.com/dwiftejb/starfiles',
    author='DwifteJB',
    license='MIT',
    author_email='dwifte@icloud.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['starfiles'],
    install_requires=['requests', 
                      ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.8',
    ],
)