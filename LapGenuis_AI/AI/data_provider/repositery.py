from AI.data_provider.parser import parse_laptops
from functools import cache
import time

CACHE_TTL = 600
last_refresh = 0

@cache
def _load_laptops():
    return parse_laptops()

def get_all_laptops():
    global last_refresh

    if time.time() - last_refresh > CACHE_TTL:
        _load_laptops.cache_clear()
        last_refresh = time.time()

    return _load_laptops().copy()