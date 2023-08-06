from setuptools import setup, find_packages


setup(
    name="pytest-fxtest",
    version="0.1.0",
    author="shuaiwang",
    install_requires=[
        "py",
        "ansi2html",
        'pytest'
    ],
    entry_points={
        "pytest11":
        [
            " pytest-fxtest= pytest_fxtest.fxtest"
        ]
    },
    url="https://github.com/shuaiwangNB/pytest-fxtest",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
