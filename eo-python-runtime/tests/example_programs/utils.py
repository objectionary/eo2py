def fibonacci(n):
    if n < 3:
        return 1
    else:
        memo = [1] * n
        for i in range(2, n):
            memo[i] = memo[i - 1] + memo[i - 2]
        return memo[n - 1]


def factorial(n):
    if n < 2:
        return 1
    else:
        return factorial(n - 1) * n
