from hashlib import sha256
import datetime as dt
from typing import Literal

time = sha256(dt.datetime.now().isoformat(timespec='milliseconds').encode(encoding='utf-8')).hexdigest()

print(time)

class one:
    def __init__(self):
        self.one = Literal[1]

obj = one()

print(obj.one == 1)

print((0.5 if 1 == 0 else -0.5))
