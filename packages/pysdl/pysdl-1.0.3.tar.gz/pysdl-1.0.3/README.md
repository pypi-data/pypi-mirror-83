# pysdl
Python Stackdriver Logger - A python library that helps Stackdriver consume python logs appropriately

## Implementing this in your app

#### In Django:
 settings.py ->
  
 ```python
    from src.pysdl import logging_dict
    LOGGING = logging_dict
```


#### In regular python apps:
 ```python
    from logging.config import dictConfig
    from src.pysdl import logging_dict
    dictConfig(logging_dict)
```