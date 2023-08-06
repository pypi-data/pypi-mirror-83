from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ml_package',
  version='0.0.5',
  description='Everything required for a ml project',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Bharat Anand',
  author_email='bharat3214@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ml', 
  packages=find_packages(),
  install_requires=['pandas == 1.1.3'] 
)