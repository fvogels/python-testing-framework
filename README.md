# Python Testing Framework

Testing framework that can be used to assign "weights" to tests.
Meant to be used in a teaching context.

## Installation

Installs in development mode:

```bash
$ pip install -e .
```

## Usage

### `Score`

A score is looks like a fraction but does **not** behave like one.
Addition of `a/b + c/d` is equal to `(a + c)/(b + d)`.

### `keep_score`

```python
with keep_score() as current_score:
    ...
    print(current_score()) # prints score of all tests ran inside the preceding block
```

### `scale`

```python
with scale(5):
    ...
```

Tests inside the block are rescaled to a score on 5.
This is added to the total score.

### `all_or_nothing`

```python
with all_or_nothing():
    ...
```

Tests inside the block are run.
If they are scored `N/N`, then this is added to the current total score.
If they are scored less, then `0/N` is added to the current total score.

### Reference Based Testing

```python
with reference_file('reference-solutions.py'):
    with reference_based_test(reference_implementation, tested_implementation) as testcase:
        testcase(inputs1)
        testcase(inputs2)
        ...
```
Runs the inputs on both implementations and increases total score if everything matches.
This includes result values and changes made to the arguments.

Shorter version, using `quick` module:

```python
with tested_tested_file('student-file.py'), reference_file('reference-implementation.py'), reference_based_test(function_name) as testcase:
    testcase(inputs1)
    testcase(inputs2)
    ...
```
