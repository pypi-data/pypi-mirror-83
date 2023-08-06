import setuptools

with open("README.md") as file:
	read_me_description = file.read()

setuptools.setup(
	name="django-firebase-custom-auth",
	version="0.1",
	author="Spider Hand",
	author_email="creative.spider.hand@gmail.com",
	description="Django backend for Firebase custom authentication.",
	long_description=read_me_description,
	long_description_content_type="text/markdown",
	url="https://github.com/spider-hand/django-firebase-custom-auth",
	packages=['django_firebase_custom_auth'],
	classifiers=[
		"Environment :: Web Environment",
		"Framework :: Django",
		"Framework :: Django :: 3.1",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
