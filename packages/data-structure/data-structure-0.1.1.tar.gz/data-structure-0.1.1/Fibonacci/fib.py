#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import sys
# 问题：求解斐波那契数列的第 n 项结果，下面以计算第40项为例
# 按照斐波那契定义来 答案102334155 执行时间30.09s
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


 # 斐波那契生成器函数，惰性计算 答案102334155 执行时间0s
def fibonacci(n):
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


# 动态规划求解，减少了数据的重复计算，每个数据只算一次 答案102334155 执行时间0s
def fib_dynamic(n):
    f, g = 0, 1
    if n <= 1:
        return n
    while(n > 1):
        g = g + f
        f = g - f
        n = n - 1
    return g


if __name__ == '__main__':

    a = 40
    old = time.time()

    # # 生成器的操作
    # result = fibonacci(a)
    # exec = 0
    # while True:
    #     try:
    #         print(next(result), end=" ")
    #     except StopIteration:
    #         sys.exit()
    #     new = time.time()
    #     exec = exec + (new - old)
    #     print(f"累计执行时间：{exec}s")

    # result = fib(a)
    result = fib_dynamic(a)
    print("计算结果：", result)
    new = time.time()
    print(f"执行时间：{new - old}s")
