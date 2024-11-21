import random
from collections import Counter


def sample(samples=1_000_000):
    def decorator(func):
        def do_random_sample(*args, **kwargs):
            result = 0
            real_samples = 0
            for i in range(samples):
                func_result = func(*args, **kwargs)
                if func_result >= 0:
                    result += func_result
                    real_samples += 1

            if real_samples > 0:
                result /= real_samples
            else:
                result = 0

            return result

        return do_random_sample

    return decorator

@sample()
def birthday_problem(n):
    birthdays = Counter(random.randint(1, 366) for _ in range(n))
    for day in birthdays:
        if birthdays[day] >= 2:
            return 1
    return 0


if __name__ == '__main__':
    n = 23

    print(f"Simulated probability of two people sharing the same birthday with {n} people: \n{100*birthday_problem(n):.3f}%")

    result = 1

    for i in range(2, n+1):
        result *= (367 - i) / 366
    result = 1 - result
    print(f"Calculated probability of two people sharing the same birthday in a room with {n} people: \n{100*result:.3f}%")