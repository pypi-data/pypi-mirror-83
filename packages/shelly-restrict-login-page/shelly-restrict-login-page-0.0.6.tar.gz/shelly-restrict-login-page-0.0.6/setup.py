from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="shelly-restrict-login-page",
    version="0.0.6",
    description="A Python package to restrict the login page of shelly-devices.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords='shelly login shelly-login shelly-restrict-login http http-requests',
    url="https://github.com/Floplosion05/Shelly",
    author="Florian Fuchs",
    author_email="florfuchs2005@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["shelly_restrict_login"],
    include_package_data=True,
    install_requires=["requests>=2.24.0", "passlib>=1.7.4"],
    entry_points={
        "console_scripts": [
            "shelly-restrict-login=shelly_restrict_login.secure:check_input",
        ]
    },
)