import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def cache_message(key, message, expiration=None):
    r.set(key, message, ex=expiration)


name = "name"
date = "15"
value = "Ваше значение"

composite_key = f"{name}:{date}"
cache_message(composite_key, value, expiration=5)

while True:
    _name = input("name")
    _date = input("date")

    key = f"{_name}:{_date}"
    retrieved_value = r.get(key)

    if retrieved_value:
        print(retrieved_value.decode("utf-8"))
    else:
        print("Значение не найдено")
        _value = input("value")
        cache_message(key, _value, expiration=10)
