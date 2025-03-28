# IMSS Payroll imss

A Python application to calculate IMSS (Mexican Social Security Institute) quotas and related payroll calculations.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/payroll-calculator.git
cd payroll-calculator
```

## Usage

1. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
python src/main.py
```

3. Run the application:

```bash
python main.py
```

## Testing

Run tests using pytest with any of the following commands:

1. Run all tests:

```bash
pytest
```

2. Run tests from a specific file:

```bash
pytest tests/test_imss.py
```

3. Run a specific test function:

```bash
pytest tests/test_imss.py::test_function_name
```

4. Run tests matching a specific pattern:

```bash
pytest -k "imss"
```

5. Run tests with detailed output:

```bash
pytest -v
```

6. Run tests and show coverage report:

```bash
pytest --cov=src tests/
```

7. Generate HTML coverage report:

```bash
pytest --cov=src tests/ --cov-report=html
```
