from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='dlight.py',
  version='0.0.4',
  description='Python api wrapper for daylight/DLIGHT',
  long_description="For docs, setup, and examples, go to https://dlight-py.gitbook.io/dlight-py/.",
  url='https://dlight-py.gitbook.io/dlight-py/',
  author='Andromeda',
  author_email='and@rjbot.xyz',
  license='MIT',
  classifiers=classifiers,
  keywords='dlight',
  packages=find_packages(),
  install_requires=['aiohttp']
)
