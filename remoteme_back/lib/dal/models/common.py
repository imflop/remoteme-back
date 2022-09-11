import typing as t
from functools import partial
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base


Base: t.Any = declarative_base()
PSQLAEnum = partial(SQLAEnum, values_callable=lambda x: [e.value for e in x])
