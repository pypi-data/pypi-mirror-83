def integer(func):
    def check(x):
        if type(x) == int:
            return func(x)
        else:
            raise Exception("expected a <type 'int'>")
    return check
def decimal(func):
    def check(x):
        if type(x) == float:
            return func(x)
        else:
            raise Exception("expected a <type 'float'>")
    return check

def string(func):
    def check(x):
        if type(x) == str:
            return func(x)
        else:
            raise Exception("expected a <type 'str'>")
    return check

def tuples(func):
    def check(x):
        if type(x) == tuple:
            return func(x)
        else:
            raise Exception("expected a <type 'tuple'>")
    return check

def lists(func):
    def check(x):
        if type(x) == list:
            return func(x)
        else:
            raise Exception("expected a <type 'list'>")
    return check

def dicts(func):
    def check(x):
        if type(x) == dict:
            return func(x)
        else:
            raise Exception("expected a <type 'dict'>")
    return check

def byte(func):
    def check(x):
        if type(x) == bytes:
            return func(x)
        else:
            raise Exception("expected a <type 'bytes'>")
    return check

def bools(func):
    def check(x):
        if type(x) == bool:
            return func(x)
        else:
            raise Exception("expected a <type 'bool'>")