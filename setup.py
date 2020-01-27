"""Installation script"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ash-model-plotting",
    version="0.0.1",
    author="Dr John A Stevenson",
    author_email="jostev@bgs.ac.uk",
    description="Simplified dispersion model result plotting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kwvmxgit.ad.nerc.ac.uk/volcanology/ash-model-plotting",
    packages=["ash_model_plotting"],
    install_requires=[],
    extras_require={
        "dev": ["flake8",
                "ipdb",
                "ipython",
                "mypy",
                "pylint",
                "pytest",
                "pytest-cov"]
    },
    entry_points={
        "console_scripts": [
            "plot_ash_model_results=ash_model_plotting.plot_ash_model_results:main",
            "name_to_netcdf=ash_model_plotting.name_to_netcdf:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: LGPLv3 License",
        "Operating System :: OS Independent",
    ],
)
