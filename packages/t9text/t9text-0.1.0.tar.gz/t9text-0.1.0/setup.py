import setuptools

try:
    with open('README.md', 'r') as rmf:
        long_description=rmf.read()
except:
    long_description='A package for handling T9 text message key mapping'


setuptools.setup(
    name='t9text',
    version='0.1.0',
    author='Brenden Hyde',
    author_email='brendenahyde@gmail.com',
    description='A package for handling T9 text message key mapping',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bxbrenden/t9text',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
