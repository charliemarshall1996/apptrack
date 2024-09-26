from setuptools import find_packages, setup

setup(
    name="apptrack",  # Your app's name
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # Includes static and template files as defined in MANIFEST.in
    license="GNU General Public License v3 (GPLv3)",  # Choose an appropriate license
    description="A Django-based job application tracking app for multiple users",
    long_description=open("README.md").read(),  # Ensure you have a README.md file
    long_description_content_type="text/markdown",
    url="https://github.com/charliemarshall1996/apptrack",  # Replace with your app’s GitHub or project page URL
    author="Charlie Marshall",
    author_email="charlie.marshall1996@gmail.com",
    install_requires=[
        "Django>=5.1",
        "psycopg2-binary>=2.9",  # Assuming you're using PostgreSQL
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",  # Specify the minimum Python version
)