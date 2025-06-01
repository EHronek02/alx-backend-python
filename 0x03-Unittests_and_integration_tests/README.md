# Unittests and Integration Tests

## Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:
- The difference between unit and integration tests.
- Common testing patterns such as mocking, parametrizations and fixtures

### Required Files
- utils.py (or download)
  Click to show/hide file contents
- client.py (or download)
  Click to show/hide file contents
- fixtures.py (or download)
  Click to show/hide file contents

# Task 0. Parameterize a unit test
Familiarize yourself with the utils.access_nested_map function and understand its purpose. Play with it in the Python console to make sure you understand.

In this task you will write the first unit test for utils.access_nested_map.

Create a TestAccessNestedMap class that inherits from unittest.TestCase.

Implement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.

Decorate the method with @parameterized.expand to test the function for following inputs:

nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
For each of these inputs, test with assertEqual that the function returns the expected result.

The body of the test method should not be longer than 2 lines.