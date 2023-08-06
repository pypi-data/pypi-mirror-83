import setuptools

with open('README', 'r') as f:
    readme = f.read()

setuptools.setup(
    name='gamepkg-jean',
    version='2.0.0',
    packages=['wargame'],
    url='https://pypi.org/legacy/gamepkg-jean',
    license='LICENSE.txt',
    description='test pkg private',
    long_description=readme,
    author='jeancarlo',
    author_email='jeantardelli@gmail.com',
    python_requires='>=3',
    )
