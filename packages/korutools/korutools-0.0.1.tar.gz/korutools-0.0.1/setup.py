import setuptools

setuptools.setup(
    name="korutools",
    version="0.0.1",
    author="Koru Tech",
    author_email="tech@koruparnters.com",
    description="A package that contains utilities for logging and notifications",
    long_description="Documentation found in https://www.notion.so/korupartners/Logging-and-Email-Notifications-611876bf43264473a0794ac699a1b84a",
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rodionlim/koru-utilities/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
