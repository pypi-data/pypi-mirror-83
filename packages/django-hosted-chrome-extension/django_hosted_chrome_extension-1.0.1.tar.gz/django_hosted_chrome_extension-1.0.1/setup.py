from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='django_hosted_chrome_extension',
    version=version,
    url='https://github.com/matix-io/django-hosted-chrome-extension',
    license='MIT',
    description='Drop-in module for a privately hosted chrome extension.',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',
    packages=find_packages(),
	include_package_data=True,
    install_requires=[],
    zip_safe=False,
    classifiers=[],
)
