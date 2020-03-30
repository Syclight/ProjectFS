from functools import update_wrapper


def accepts(*types):
    def check_accepts(f):
        def new_f(*args, **kwds):
            assert len(types) == (len(args) + len(kwds)), \
                "args cnt %d does not match %d" % (len(args) + len(kwds), len(types))
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                    "arg %r does not match %s" % (a, t)
            return f(*args, **kwds)

        update_wrapper(new_f, f)
        return new_f

    return check_accepts


def returns(rtype):
    def check_returns(f):
        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            assert isinstance(result, rtype), \
                "return value %r does not match %s" % (result, rtype)
            return result

        update_wrapper(new_f, f)
        return new_f

    return check_returns


@accepts(int, (int, float))
@returns((int, float))

def func(arg1, arg2):
    return arg1 * arg2

if __name__ == "__main__":
    a = func(1, 'b')
    print(a)