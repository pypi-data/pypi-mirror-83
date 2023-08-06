import setuptools

setuptools.setup(
    name="jenkins-handler",
    version="1.0.5.1",
    author="Deep Instinct",
    author_email="tomerco@deepinstinct.com",
    description="A Wrapper for Jenkins API",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    py_modules=['jenkins_job', 'jenkins_logs_parser'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
