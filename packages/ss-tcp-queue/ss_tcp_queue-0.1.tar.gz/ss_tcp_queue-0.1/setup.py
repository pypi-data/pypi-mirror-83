from distutils.core import setup
setup(
  name = 'ss_tcp_queue',     
  packages = ['ss_tcp_queue'],   
  version = '0.1',      
  license='MIT',        
  description = 'Custom Datadog agent check for collecting TCP queue metrics using "ss" command',
  author = 'adulmovits',
  author_email = 'suddenjihadsyndrome@gmail.com',
  url = 'https://github.com/adulmovits/ss_tcp_queue', 
  download_url = 'https://github.com/adulmovits/ss_tcp_queue/archive/main.zip',
  install_requires=[], 
  classifiers=[
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3'
  ],
)
