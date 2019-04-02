from abc import ABCMeta, abstractmethod
from cachetools import cached, TTLCache


class Fibonacci(metaclass=ABCMeta):  # Abstract prototype ######################
    def fibonacci(self, n):
        if isinstance(n, int) and n >= 0:
            return self._fibonacci(n) if n >= 2 else [0, 1][n]
        raise ValueError

    @abstractmethod
    def _fibonacci(self, n):
        pass


class FibonacciRecursion(Fibonacci):  # 1. Classic and also naive computation ##
    def _fibonacci(self, n):
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)


class FibonacciCacheTools(Fibonacci):  # 2. The cache fixes bad algorithm choice
    cache = TTLCache(maxsize=1500, ttl=3600)

    @cached(cache)
    def _fibonacci(self, n):
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)


class FibonacciAddition(Fibonacci):  # 3. It is O(n), not O(2**n) as before ####
    def _fibonacci(self, n):
        f0, f1 = 0, 1
        for _ in range(1, n):
            f0, f1 = f1, f0 + f1
        return f1


class FibonacciAdditionPlus(Fibonacci):  # 4. Exploiting the sequential n: O(1)
    def __init__(self):
        self._n = 2
        self._f0 = 1
        self._f1 = 1

    def _fibonacci(self, n):
        if n == self._n:
            return self._f1
        if n < self._n:
            self.__init__()
        for _ in range(self._n, n):
            self._f0, self._f1 = self._f1, self._f0 + self._f1
        self._n = n
        return self._f1


class FibonacciFormula(Fibonacci):  # 5. Formula of Binet, Moivre, and Bernoulli
    # Exact integer until Fibonacci(71)
    # Float error at Fibonacci(1475)  OverflowError: (34, 'Result too large')
    S5 = 5.0 ** 0.5  # Square root of 5

    def _fibonacci(self, n):
        phi = (1.0 + FibonacciFormula.S5) / 2.0  # φ Python speaks greek!
        psi = (1.0 - FibonacciFormula.S5) / 2.0  # ψ PyCharm doesn't like it ;-(
        return int((phi ** n - psi ** n) / FibonacciFormula.S5)


if __name__ == '__main__':  # Testing ... ######################################
    import platform
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit

    def func1(x, a, b):  # function to fit exponential Fibonacci
        return '%f * %f**x' % (a, np.exp(b)) if x is None else a*np.exp(b*x)

    def func2(x, a, b, c):  # function to fit with cubic curve
        return '%f + %f*x + %f*x**2' % (a, b, c) if x is None else a+x*(b+c*x)

    def first_test(fibonacci_max, repeat):  # Collect times, curve fit, and plot
        methods = [  # Function to test, color, poly fit, curve fit
            [FibonacciRecursion(),    'blue',   2, func1],
            [FibonacciCacheTools(),   'orange', 1, func2],
            [FibonacciAddition(),     'green',  1, func2],
            [FibonacciAdditionPlus(), 'red',    1, func2],
            [FibonacciFormula(),      'purple', 1, func2],
        ]
        print('Number,Fibonacci,Times for all methods in nanoseconds')
        n_max = fibonacci_max - 1  # we start from n=2 (0, 1 - the same time)
        y = [[0 for _ in range(n_max)] for _ in methods]
        for j in range(n_max):  # Run tests and collect times in array y #######
            n = j + 2
            old = None
            for i, method in enumerate(methods):
                best = None
                for k in range(repeat):
                    start = time.perf_counter_ns()
                    result = method[0].fibonacci(n)
                    stop = time.perf_counter_ns()
                    duration = stop - start
                    if best is None or duration < best:
                        best = duration
                    if old is None:
                        old = result
                    elif result != old:
                        print(
                            'Error: different results %d and %d for function %s'
                            ' F(%d) in call # %d,' %
                            (old, result, method[0].fibonacci.__name__, n, k+1))
                        exit(1)
                if i == 0:
                    print(n, ',', old, sep='', end='')
                print(',', best, sep='', end='')
                y[i][j] = best
            print()
        plt.figure(1)  # Start plotting ########################################
        plt.suptitle('Time(n) Complexity of Fibonacci Algorithms. n = 2,3,...,'
                     '%d,%d' % (n_max, fibonacci_max))
        x = np.array([i + 2 for i in range(n_max)])
        plt.subplots_adjust(hspace=0.3)
        for i in range(4):
            plt.subplot(221 + i)
            for j, m in enumerate(methods):
                s = str(m[0].__class__.__name__)[len('Fibonacci'):]
                plt.plot(x, y[j], 'tab:' + m[1], label=s)
            plt.title(['time in nanoseconds', 'log(Time)', 'zoom', 'zoom+'][i])
            plt.grid(True)
            if i == 0:
                plt.legend()
            elif i == 1:
                plt.semilogy()
            else:
                x_min, x_max, _, _ = plt.axis()
                plt.axis([x_min, x_max, 0.0, 30000.0 if i == 2 else 3000.0])
        for i, m in enumerate(methods):  # Curve and poly fitting ##############
            plt.figure(2 + i)
            name = str(m[0].__class__.__name__)[len('Fibonacci'):]
            plt.plot(x, y[i], 'ko', label=name)
            c, _ = curve_fit(m[3], x, y[i])
            c_name = 'curve fit:' + m[3](None, *c)
            plt.plot(x, m[3](x, *c), 'y-', label=c_name)
            p = np.poly1d(np.polyfit(x, y[i], m[2]))
            p_name = 'poly fit: ' + str(p)
            plt.plot(x, p(x), m[1], label=p_name)
            plt.legend()
            print('%s\n%s\n%s\n' % (name, c_name, p_name))
        plt.show()

    print('Python version  :', platform.python_version())
    print('       build    :', platform.python_build())
    print('       compiler :\n', platform.python_compiler())
    first_test(fibonacci_max=30, repeat=10)
