from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

with open('README.md') as f:
    readme = f.read()

# print(find_packages(exclude=('examples')))
# print(license)

setup(
    name='degiropy',
    version='0.1.1',
    description='Unofficial Degiro API in python',
    url='https://github.com/alexberazouski/degiropy',
    author='Alex Berazouski',
    author_email='alex.berazouski@gmail.com',
    license=license,
    packages=find_packages(exclude=('examples')),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD 2 License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False
)
