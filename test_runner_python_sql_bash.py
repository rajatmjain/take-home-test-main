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

