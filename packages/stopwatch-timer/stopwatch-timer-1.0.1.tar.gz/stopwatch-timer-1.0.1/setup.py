import setuptools
with open("README.md") as f:
    long_text = f.read()
setuptools.setup(name="stopwatch-timer",
                 version="1.0.1",
                 author="Benjamin Richter",
                 description="A stopwatch class that can be used as a timer.",
                 long_description=long_text,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Development Status :: 5 - Production/Stable",
                     "License :: OSI Approved :: MIT License",
                     "Natural Language :: English",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3"],
                 python_requires=">=3")
