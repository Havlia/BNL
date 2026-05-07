from hashlib import sha256
import datetime as dt
from typing import Literal

time = sha256(dt.datetime.now().isoformat(timespec='milliseconds').encode(encoding='utf-8')).hexdigest()

print(time)
def balls():

    with open('r', 'r'):
        pass

