from setuptools import setup, find_packages

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""

setup(
				name='hummus2016.py',
				version='0.4.0',
				author='LG125YT',
				author_email='lg125yt@gmail.com',
				description='An asynchronous API wrapper for Hummus by Ziad87',
				long_description=open('README.md').read(),
				long_description_content_type='text/markdown',
				url='https://gitlab.com/lg125yt/hummus.py',
				packages=find_packages(),
				install_requires=[
								"discord.py",
								"asyncio",
								"fake_useragent",
								"websockets",
								"requests"
				],
				classifiers=[
								'Development Status :: 3 - Alpha',
								'Intended Audience :: Developers',
								'License :: OSI Approved :: MIT License',
								'Operating System :: OS Independent',
								'Programming Language :: Python',
								'Programming Language :: Python :: 3',
								'Programming Language :: Python :: 3.6',
								'Programming Language :: Python :: 3.7',
								'Programming Language :: Python :: 3.8',
								'Programming Language :: Python :: 3.9',
								'Programming Language :: Python :: 3.10',
								'Programming Language :: Python :: 3.11',
				],
)