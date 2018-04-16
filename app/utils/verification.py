import random


def generate_code():
    return ''.join(str(random.choice(range(1, 7))) for _ in range(6))


if __name__ == "__main__":
    print(generate_code())
