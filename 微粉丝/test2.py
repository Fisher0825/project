import time
# def timer(func):
#
#     def inner():
#         start_time = time.time()
#         print(start_time)
#         func()
#         end_time = time.time()
#         print(end_time-start_time)
#
#     return inner
# @timer#相当于func1 = timer(func1)
# def func1():
#     time.sleep(2)
#     # print('this is func1')
# func1()

# import time
# def timer(func):
#     def inner(*args,**kwargs):
#         start = time.time()
#         re = func(*args,**kwargs)
#         print(time.time() - start)
#         return re#这里的返回值re就是func的返回值，如果不是re，那么就不返回func的返回值
#     return inner
#
# @timer   #==> func2 = timer(func2)
# def func2(a):
#     time.sleep(1)
#     print('in func2 and get a:%s'%(a))
#     return 'fun2 over'
#
# # func2('aaaaaa')
# print(func2('aaaaaa'))

#
# def index():
#     '''这是一个主页信息'''
#     print('from index')
#
# print(index.__doc__)    #查看函数注释的方法def wrapper1(func):
#

# def wrapper1(func):
#     def inner():
#         print('wrapper1 ,before func')
#         func()
#         print('wrapper1 ,after func')
#     return inner
#
# def wrapper2(func):
#     def inner():
#         print('wrapper2 ,before func')
#         func()
#         print('wrapper2 ,after func')
#     return inner
#
# @wrapper2
# @wrapper1
# def f():
#     print('in f')
# f()



import time
# def genrator_fun1():
#     a = 1
#     print('现在定义了a变量')
#     yield a
#     b = 2
#     print('现在又定义了b变量')
#     yield b
# g1 = genrator_fun1()
# print('g1 : ',g1)       #打印g1可以发现g1就是一个生成器
# print('-'*20)   #我是华丽的分割线
# print(next(g1))
# time.sleep(5)   #sleep一秒看清执行过程
# print(next(g1))
#
# li = [1,2,3,4,5]
# print(li.index(1))
# def findMinAndMax(L):
#     if len(L)==0:
#         Min,Max = None,None
#     elif len(L)==1:
#         Min,Max = L[0],L[0]
#     else:
#         Min,Max = L[0],L[0]
#         for i in L[1:]:
#             if i <= Min:
#                 Min=i
#             elif i >= Max:
#                 Max=i
#     return (Min,Max)

L1 = ['Hello', 'World', 18, 'Apple', None]
# for i in L1.__iter__():
#     print(i)

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
f = fib(10)
fb = f.__iter__()
# print(fb.__iter__() == fb)
# f.__next__()
from collections import Iterator
print(isinstance(f,Iterator))
print(isinstance(L,Iterator))
