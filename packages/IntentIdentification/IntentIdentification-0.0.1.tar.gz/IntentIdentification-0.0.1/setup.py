import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IntentIdentification", 
    version="0.0.1",
    author="Shreyansh Das",
    author_email="shreyanshdas00@gmail.com",
    description="A package to detect intent from utterances.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/AlphaDino/commercebot/-/tree/master/Direct%20Contact%20Intent%20Detection",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[            
          'numpy',
          'torch',
          'tqdm',
          'transformers',
          'ordered_set'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)