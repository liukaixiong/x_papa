def fib():
    for i in range(10):
        print("||||||||||" + str(i) + "||||||||||")
        yield str(i)
        print("----------------" + str(i) + "-------------------")
        yield (i + 1)
        print("================" + str((i + 1)) + "================")


# 字符串
astr = 'ABC'
# 列表
alist = [1, 2, 3]
# 字典
adict = {"name": "wangbm", "age": 18}
# 生成器
agen = (i for i in range(4, 8))


def gen(*args, **kw):
    for item in args:
        for i in item:
            yield i


def gen_from(*args, **kw):
    for i in args:
        yield from i


new_list = gen_from(astr, alist, adict, agen)
print(list(new_list))
# ['A', 'B', 'C', 1, 2, 3, 'name', 'age', 4, 5, 6, 7]

# if __name__ == '__main__':
# i = fib()
# print(next(i))
# print(next(i))
# print(next(i))
# print(next(i))
# print(next(i))
