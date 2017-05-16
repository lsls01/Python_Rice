Difference between type and isinstance
------
    class Foo(object):
        pass
    class Bar(Foo):
        pass
    print type(Foo()) == Foo
    print type(Bar()) == Foo
    print isinstance(Bar(), Foo)
#### output:
#### True, False, True
