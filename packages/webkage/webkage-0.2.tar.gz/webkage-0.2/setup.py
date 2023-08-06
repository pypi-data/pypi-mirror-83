from distutils.core import setup
setup(
  name = 'webkage',
  packages = ['webkage'],
  version = '0.2',
  license='MIT',
  description = 'A lightweight webframework',
  author = 'Oloruntobi Balogun',
  author_email = 'tobitobitobiwhy@gmail.com',
  url = 'https://github.com/laybug/webkage',
  download_url = 'https://github.com/LayBug/webkage/archive/v0.2.tar.gz',
  keywords = ['Framework', 'Web', 'Wsgi'],
  install_requires=[
          'jinja2'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',   
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    
  ],
)
