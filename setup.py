from setuptools import setup, find_packages

setup(
    name="payroll_calculator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "xlsxwriter",
        "tabulate",
    ],
    author="Anonimo Tech",
    author_email="tu@email.com",
    description="A package for calculating IMSS, ISR, and savings for Mexican payroll",
    keywords="payroll, imss, isr, mexico, taxes",
    url="https://github.com/tuusuario/payroll-calculator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)