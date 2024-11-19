import random


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
def simulation():
    box1 = ["red"] * 7 + ["green"] * 2
    box2 = ["red"] * 3 + ["green"] * 4
    boxes = [box1, box2]
    chosen_box = random.randint(0, 1)
    box = boxes[chosen_box]
    chosen_ball = random.choice(box)

    if chosen_ball != "red":
        return -1

    return chosen_box == 0


print(f"Probability of ball being in box 1 given it is red: {100*simulation():.4f}%")
