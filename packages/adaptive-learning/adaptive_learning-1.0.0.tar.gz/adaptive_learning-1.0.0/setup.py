import io
from setuptools import setup, find_packages



setup(
    name='adaptive_learning',
    version='1.0.0',
    author='shivachandra',
    author_email='k.s9908725092@gmail.com',
    url='https://github.com/shivachandrakante/Adaptive-Learning',
    description='An awesome package which helps us in Learning throughs quizes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='sqlite database quiz adaptive learning',
    packages=find_packages(),
    license='LICENSE',
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    include_package_data=True,
    install_requires=
      [
        "tkinter",
        "sqlite",
      ],
)