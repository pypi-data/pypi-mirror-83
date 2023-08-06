from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
      name='cartoonizer',
      version='0.0.3',
      description='Convert your Image into a Cartoon form',
      py_modules=["cartoonizer"],
      package_dir={'':'cartoonizer'},
      long_description = long_description,
      long_description_content_type="text/markdown",
      install_requires=["numpy","cv2","scipy",]
)