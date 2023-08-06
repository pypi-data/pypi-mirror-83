from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="notifstats",
    packages=["notifstats"],
    python_requires=">=3.6",
    version="0.0.6",
    license="MIT",
    description="Notification statistic collector",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="I Putu Alfred Crosby",
    author_email="alfred.crosby@kumparan.com",
    url="https://github.com/kumparan/notification-stats",
    download_url="https://github.com/kumparan/notification-stats/archive/v_01.tar.gz",
    keywords=[
        "Notification Statistic",
        "Kumparan",
    ],
    install_requires=["google-cloud-bigquery>=1.20.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)