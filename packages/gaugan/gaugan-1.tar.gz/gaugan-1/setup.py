import setuptools

with open('README.md', 'r') as f:
	long_description = f.read()

setuptools.setup(
	name='gaugan',
	version='1',
	author='Erik Keresztes',
	author_email='erik@erik.cash',
	description='An interface for NVIDIA\'s gauGAN project that turns crude drawings into realistic images using AI.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/erikKeresztes/gaugan.py',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
		"Operating System :: OS Independent"
	],
	python_requires='>=3'
)
