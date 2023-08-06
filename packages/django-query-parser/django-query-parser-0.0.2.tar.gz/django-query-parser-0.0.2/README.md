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
      ```pytho
   {"status_id" : 3, "name__icontains":"Ahmed"}
   ```
  ## Installation
  `pip install django-query-parser`
