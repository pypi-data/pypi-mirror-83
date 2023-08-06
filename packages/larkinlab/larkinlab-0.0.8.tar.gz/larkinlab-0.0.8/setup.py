from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='larkinlab',
    version='0.0.8',
    description='A package of code to make things easier',
   # long_description= open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Conor Larkin',
    author_email='conor.larkin16@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='data',
    packages=find_packages(),
    install_requires=["pandas","matplotlib"]
)