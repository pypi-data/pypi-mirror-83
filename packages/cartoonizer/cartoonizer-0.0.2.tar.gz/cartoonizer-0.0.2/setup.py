from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
      name='cartoonizer',
      version='0.0.2',
      description='Convert your Image into a Cartoon form',
      py_modules=["cartoonizer"],
      package_dir={'':'cartoonizer'},
      long_description = long_description,
      long_description_content_type="text/markdown",
      classifier=["Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6","Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Programming Language :: Python :: 3.9", 
                  "License :: OSI Approved :: Apache Software License", 
                  "Operating System :: OS Independent"],
      install_requires=["numpy","cv2","scipy",]
)