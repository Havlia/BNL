from hashlib import sha256
import datetime as dt

time = sha256(dt.datetime.now().isoformat(timespec='milliseconds').encode(encoding='utf-8')).hexdigest()

print(time)



print(dt.datetime.now() == dt.datetime.now())
