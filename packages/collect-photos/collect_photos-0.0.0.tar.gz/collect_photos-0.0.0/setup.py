import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='collect_photos',
    version="0.0.0",
    install_requires=requirements,
    author="Matthew Wen",
    author_email="mattwen2018@gmail.com",
    description="Uploading Files to AWS S3 and Logging it into DynamoDB",
    packages=setuptools.find_packages(),
    scripts=["bin/collect-photos"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
