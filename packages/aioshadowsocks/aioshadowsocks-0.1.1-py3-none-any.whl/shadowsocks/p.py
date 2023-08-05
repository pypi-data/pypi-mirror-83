from functools import wraps

import cProfile
from line_profiler import LineProfiler

import time


def func_time(f):
    """
    简单记录执行时间
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, "took", end - start, "seconds")
        return result

    return wrapper


def func_cprofile(f):
    """
        内建分析器
      194 function calls (189 primitive calls) in 0.000 seconds
    Ordered by: standard name
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
         1    0.000    0.000    0.000    0.000 re.py:188(compile)
         1    0.000    0.000    0.000    0.000 re.py:226(_compile)
    1. 第一行告诉我们一共有194个函数被调用，其中189个是原生（primitive）调用，表明这些调用不涉及递归。
    2. ncalls表示函数的调用次数，如果这一列有两个数值，表示有递归调用，第一个是总调用次数，第二个是原生调用次数。
    3. tottime是函数内部消耗的总时间（不包括调用其他函数的时间）。
    4. percall是tottime除以ncalls，表示每次调用平均消耗时间。
    5. cumtime是之前所有子函数消耗时间的累积和。
    6. percall是cumtime除以原生调用的数量，表示该函数调用时，每个原生调用的平均消耗时间。
    7. filename:lineno(function)为被分析函数所在文件名、行号、函数名。
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = f(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort="time")

    return wrapper


def func_line_time(follow=[]):
    """
        每行代码执行时间详细报告
        :param follow: 内部调用方法
        :return:
        Timer unit: 1e-06 s
    Timer unit: 1e-06 s
    Total time: 14.4183 s
    File: /xx/test.py
    Function: test at line 41
    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
    41                                           @func_line_time()
    42                                           def test():
    43  10000001    4031936.0      0.4     28.0      for x in range(10000000):
    44  10000000   10386347.0      1.0     72.0          print x
    Total Time：测试代码的总运行时间
    Line:代码行号
        Hits：表示每行代码运行的次数
        Time：每行代码运行的总时间
        Per Hits：每行代码运行一次的时间
        % Time：每行代码运行时间的百分比
    """

    def decorate(func):
        @wraps(func)
        def profiled_func(*args, **kwargs):
            try:
                profiler = LineProfiler()
                profiler.add_function(func)
                for f in follow:
                    profiler.add_function(f)
                profiler.enable_by_count()
                return func(*args, **kwargs)
            finally:
                profiler.print_stats()

        return profiled_func

    return decorate
