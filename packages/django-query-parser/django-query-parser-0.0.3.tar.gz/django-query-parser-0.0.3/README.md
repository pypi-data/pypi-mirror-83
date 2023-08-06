# django-query-parser
A django app to parse queries written outside the django app.

## Idea
Some queries are controls the business case, so it will be benefical if they are can saved outside the application like in a config file or a database so the logic can be changed without changing the code.

## Samples
1. to write an 'or'
   ```python
    {"or":{"status_id" : 3, "name__icontains":"Ahmed"}}
   ```
2. to write negation
    ```python
    {"or":{"status_id" : 3, "~name__icontains":"Ahmed"}}
   ```
3. to write an 'and'
   ```python
    {"and":{"status_id" : 3, "name__icontains":"Ahmed"}}
   ```
   or
   ```python
   {"status_id" : 3, "name__icontains":"Ahmed"}
   ```
## Installation
  `pip install django-query-parser`

## Example

from test_app
 ```python
from query_parser.Parser import  Parse
d = {"or": {
    "status": "Completed",
    "ordered_by_id": 2
    }}
res = Parse(d)
print(Order.objects.filter(res).count())
```

## Operation Supported
1. AND
2. OR
3. NOT: with a '~' in field name 
   example
   ```python 
   d = {"status": "Completed", "~ordered_by_id": 1}
   ```