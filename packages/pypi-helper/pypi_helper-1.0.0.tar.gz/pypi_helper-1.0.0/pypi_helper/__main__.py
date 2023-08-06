### IMPORTS             ###
    ## Dependencies         ##
    ## Dependencies         ##
import os
import pypi_helper
import datetime
### IMPORTS             ###

if __name__ == "__main__":
    import sys
    setup_cmd = sys.argv[1]      # Path to package
    if setup_cmd != "setup": raise pypi_helper.ArgumentException(setup_cmd)

    author, email = '', ''
    while author == '': author = input('Author: ')
    while email == '': email = input('Email: ')

    path, package, package_desc, dependencies = '', '', '', ''
    while path == '': path = input('Path to project directory: ')
    while package == '': package = input('Package name: ')
    while package_desc == '': package_desc = input('Package Description: ')
    while dependencies == '': dependencies = input('Dependencies: ')
    dependencies = dependencies.split(',')
    dependencies = [i.strip() for i in dependencies]
    new_deps = []
    for idx, i in enumerate(dependencies):
        if i != '': new_deps.append(i)
    else: dependencies = new_deps
    os.chdir(path) if path != 'here' else print('')
    requirements_txt = input('Include requirements.txt (y/n): ')
    requirements_txt = 'y' if requirements_txt == '' else requirements_txt
    try: os.mkdir('tests')       # tests dir
    except FileExistsError: print("'tests' directory already exists. Skipped.")
    with open('LICENSE', 'w') as f:
        f.write(
            f"""
Copyright (c) {datetime.date.today().year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
            """
        )

    with open('setup.py', 'w') as f:
        f.write(
            f"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="{package}",
    version="0.0.1",
    author="{author}",
    author_email="{email}",
    description="{package_desc}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.beyonce.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = {dependencies}
)
            """
        )

    with open('requirements.txt', 'a') as f:
        for dep in dependencies: f.write(dep)