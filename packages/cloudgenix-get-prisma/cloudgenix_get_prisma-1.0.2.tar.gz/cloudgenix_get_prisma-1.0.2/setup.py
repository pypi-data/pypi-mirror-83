from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='cloudgenix_get_prisma',
      version='1.0.2',
      description='Utility to print or export all CloudGenix ServiceLinks to Prisma.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ebob9/cloudgenix_get_prisma',
      author='Aaron Edwards',
      author_email='cloudgenix_get_prisma@ebob9.com',
      license='MIT',
      install_requires=[
            'cloudgenix >= 5.4.1b2',
            'cloudgenix_idname >= 2.0.1',
            'tabulate >= 0.8.7'
      ],
      packages=['cloudgenix_get_prisma'],
      entry_points={
            'console_scripts': [
                  'get_prisma_servicelinks = cloudgenix_get_prisma:go',
                  ]
      },
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
      ]
      )
