
def flatten(a):
    if not isinstance(a, list) and not isinstance(a, tuple):
        return [a] if a is not None else []

    if len(a) == 2:
        if isinstance(a[0], list) or isinstance(a[0], tuple):
            res = flatten(a[0])
        else:
            res = a[0]
        res = [res] + flatten(a[1])
        # print("flatten {}: got {}".format(a, res))
        return res
