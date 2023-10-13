import pytest
from ploomber_test.runner import CodeRunner

code_text = """
```python
print("Hello, Python!")
```

```sql
SELECT * from numbers;
```

```bash
echo "Hello, Bash!"
```
"""

def test_runner_python_sql_bash():
    runner = CodeRunner(code_text)
    runner.run()

@pytest.mark.python
def test_runner_python():
    code = """
    python```
    print("Hello, Python!")
    ```
    """
    runner = CodeRunner(code)
    runner.run()

@pytest.mark.sql
def test_runner_sql():
    code = """
    sql```
    SELECT * FROM my_table;
    ```
    """
    runner = CodeRunner(code)
    runner.run()

@pytest.mark.bash
def test_runner_bash():
    code = """
    bash```
    echo "Hello, Bash!"
    ```
    """
    runner = CodeRunner(code)
    runner.run()