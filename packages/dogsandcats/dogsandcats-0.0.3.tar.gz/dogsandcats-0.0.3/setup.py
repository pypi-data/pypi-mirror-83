from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7'
]
 
setup(
  name='dogsandcats',
  version='0.0.3',
  description='Dataset package for dogs and cats classification problem ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',  
  author='Veeresh Ittangihal',
  author_email='valiant.veeru@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dataset', 
  packages=find_packages(),
  install_requires=['numpy', 'scikit-image'],
  python_requires='>=3.6'
)