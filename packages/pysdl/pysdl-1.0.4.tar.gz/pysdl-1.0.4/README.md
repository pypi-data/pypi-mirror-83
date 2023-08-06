# pysdl
Python Stackdriver Logger - A python library that helps Stackdriver consume python logs appropriately

## Installing pysdl
```bash
pip install pysdl 
```

## Implementing this in your app

#### In Django:
 settings.py ->
  
 ```python
from pysdl.logger_config import logging_dict

LOGGING = logging_dict
```


#### In regular python apps:
 ```python
from logging.config import dictConfig
from pysdl.logger_config import logging_dict

dictConfig(logging_dict)
```