from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='degiropy',
    version='0.1.2',
    description='Unofficial Degiro API in python',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/alexberazouski/degiropy',
    author='Alex Berazouski',
    author_email='alex.berazouski@gmail.com',
    license='BSD 2',
    packages=find_packages(exclude=('examples')),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False
)
