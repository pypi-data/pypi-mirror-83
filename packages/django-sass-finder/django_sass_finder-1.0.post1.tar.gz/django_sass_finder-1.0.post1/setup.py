import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_sass_finder",
    version="1.0.post1",
    author="Jesus Trujillo",
    author_email="trudev.professional@gmail.com",
    description="a Django finder that compiles Sass files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tru-Dev/django_sass_finder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
    ],
    python_requires='>=3.6',
)
