

To add new router:
- extend `routers` directory in main.py
- create new routers file in app/src/api/


To get database instance:

from anywhere in the code:
```python
from src.utils import database
```

from router:
```python
from fastapi import APIRouter

router = APIRouter
# ...
database = router.database
```

