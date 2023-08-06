import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="python-sendmail",
    version="0.3.1",
    description="Sendmail client. send mail via stmp server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zencore-cn/zencore-issues",
    author="zencore-cn",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["python-sendmail", "pysendmail", "sendmail", "pysendeml", "sendeml", "mail"],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["sendmail"],
    entry_points={
        "console_scripts": [
            "pymail = sendmail:main",
            "pysendeml = sendmail:sendeml_cmd",
            "pysendmail = sendmail:sendmail_cmd",
            "pymakemail = sendmail:makemail_cmd",
        ]
    },
)