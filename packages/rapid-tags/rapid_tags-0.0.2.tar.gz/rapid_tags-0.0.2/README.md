# rapid_tags

![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/rapid_tags?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/rapid_tags)

## Description

python wrapper for rapidtags.io

## Install

~~~~bash
pip install rapid_tags
# or
pip3 install rapid_tags
~~~~

## Usage

```python
from rapid_tags import RapidTags

print(RapidTags.get_tags_cls('python programming'))
# prints: ['python programming', 'python', 'python tutorial', 'learn python', 'python programming language', 'programming', 'learn python programming', 'python (programming language)', 'python programming tutorial', 'python for beginners', 'python tutorial for beginners', 'python basics', 'python course', 'python language', 'expert python programming', 'python programming course', 'python programming in hindi', 'why learn python programming', 'python full course', 'python programming for beginners', 'python crash course', 'python from scratch', 'programming tutorial']
```
