from setuptools import setup, find_packages


def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


def get_requires():
    try:
        with open("requirements.txt", "r") as req:
            install_requires = [item.strip() for item in req.readlines()]
    except FileNotFoundError:
        with open("marshmallow_advanced.egg-info/requires.txt", "r") as req:
            install_requires = [item.strip() for item in req.readlines()]
    return install_requires


setup(name='marshmallow_advanced',
      version='1.2.0',
      url='https://github.com/maximshumilo/marshmallow_advanced',
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      description='Lib marshmallow advanced',
      packages=find_packages(),
      author='Shumilo Maksim',
      author_email='shumilo.mk@gmail.com',
      install_requires=get_requires(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3.8",
          "Intended Audience :: Developers",
          'Topic :: Software Development',
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.8',
      zip_safe=False)

