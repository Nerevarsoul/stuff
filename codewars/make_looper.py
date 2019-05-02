
def make_looper(s):
    def gen(st):
        while True:
            for i in st:
                yield i
    a = gen(s)

    def abc():
        return next(a)
    return abc
