from setuptools import setup

setup(
    name="dxxtools",
    version="0.1.0",
    description="dxxtools is a package of useful tools for .DXX",
    install_requires=["dxx", "numpy", "matplotlib"],
    entry_points={
        "console_scripts": [
            "vs_plot = dxxtools.vs_plot:main"
            "upsampling = dxxtools.upsampling:main"
        ]
    },
    author="Tetsu Takizawa",
    author_email="tetsu.varmos@gmail.com",
    url="https://github.com/tetsuzawa/spatial-research/tree/master/modules/dxxtools"
)
