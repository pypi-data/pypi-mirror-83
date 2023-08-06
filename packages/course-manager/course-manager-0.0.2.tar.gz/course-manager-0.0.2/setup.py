import setuptools


with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="course-manager",
    version="0.0.2",
    author="Asad Moosvi",
    author_email="moosvi.asad@gmail.com",
    description="Keep track of the courses you're taking",
    url="https://github.com/asadmoosvi/course-manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["course_manager=course_manager.cli:main"]
    }
)
