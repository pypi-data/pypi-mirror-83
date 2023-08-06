Pytest Allure DSL Plugin
========================

Installation
------------

```bash
pip install pytest-allure-dsl
```

Enable plugin
-------------

From command line

```bash
pytest -p pytest_allure_dsl --allure-dsl
```

From pytest.ini

```ini
[pytest]
addopts = -p pytest_allure_dsl --allure-dsl
```

From conftest.py

```python
pytest_plugins = ['pytest_allure_dsl']
```

By default allure dir is **./.allure**, you can change it with **--alluredir** option

Usage
-----

```python
"""
feature:
  - common feature from module to test case functions
"""


def test_example(allure_dsl):
    """
    story: test story string or story list
    description: test description string
    issue: issue for example
    steps:
      1: step {num}
      2: step two
    """
    with allure_dsl.step(1, num='one'):
        pass

    with allure_dsl.step(2):
        pass


class TestExample:
    """
    feature:
      - common feature from class to test case methods
    """

    def test_example(self):
        """
        story: test story string or story list
        description: test description string
        attachments:
          - title: jsonschema
            file: jsonschemaes/schema.json
        """
        pass
```

Top level labels
-----------------

* feature
* story
* epic
* issue
* link
* test_case

