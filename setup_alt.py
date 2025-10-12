from setuptools import find_packages, setup

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""

setup(
				name='hmus',
				version='1.1.4',
				author='LG125YT',
				author_email='lg125yt@gmail.com',
				description='An asynchronous API wrapper for Hummus by Ziad87',
				long_description=open('README.md').read(),
				long_description_content_type='text/markdown',
				url='https://github.com/LG125YT/Hummus.py',
				packages=find_packages(),
				install_requires=[
					"datetime",
					"asyncio",
					"fake_useragent",
					"websockets",
					"requests",
					"requests_toolbelt",
					"filetype",
					"Pillow",
					"typing"
				],
				classifiers=[
								'Development Status :: 4 - Beta',
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
