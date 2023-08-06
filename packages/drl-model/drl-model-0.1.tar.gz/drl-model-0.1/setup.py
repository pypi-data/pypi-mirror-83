import setuptools

setuptools.setup(
    name="drl-model", # Replace with your own username
    version="0.01",
    author="author-drl",
    author_email="author-drl@example.com",
    description="DRL logic",
    long_description="drl",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          "numpy>=1.16.4",
        "pandas>=1.0.3",
        "stockstats",
        "scikit-learn>=0.21.0",
        "gym>=0.15.3",
        "stable-baselines[mpi]",
        "coloredlogs",
        "ray[all]",
        "tensorflow-gpu==1.14",
        "ax-platform==0.1.14",
        "joblib>=0.15.1",
        "matplotlib>=3.2.1",
        "botorch",
       "ta>=0.5.25",
        "yfinance",
        "quantstats",
        "TA-Lib>=0.4.19"
      ],
    python_requires='==3.7',
)