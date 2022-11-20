from enum import Enum


class Score(Enum):
    CORRECT = 5
    WRONG = 0
    WIN = 20
    LOSE = 0


if __name__ == "__main__":
    print(Score.CORRECT.value)
    a = ["1234", "12345", "123456", "1234567"]
    b = filter(lambda x: len(x) < 5, a)
    print(list(b))
