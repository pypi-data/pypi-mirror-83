    
from distutils.core import setup

version_number = '0.0.1'
package_name = 'c355'
package_description = 'Shes the whole dang package'
search_tags = package_name.split("-") + []

setup(
  name = package_name,    
  packages = [package_name],   
  version = version_number,
  license = 'MIT',        
  description = package_description, 
  author = 'Ryan Schreiber',   
  author_email = 'ryanschreiber86@gmail.com', 
  url = f'https://github.com/ryan-schreiber/{package_name}',  
  download_url = f'https://github.com/ryan-schreiber/{package_name}/archive/{version_number}.tar.gz',
  keywords = search_tags,
  install_requires=[
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)


