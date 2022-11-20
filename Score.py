from enum import Enum


class Score(Enum):
    


    @staticmethod
    def CORRECT():
        return 5

    @staticmethod
    def WRONG():
        return 0

    @staticmethod
    def LOSE():
        return 0

    @staticmethod
    def WIN():
        return 10


if __name__ == "__main__":
    print(Score.CORRECT())
    a = ["1234", "12345", "123456", "1234567"]
    b = filter(lambda x: len(x) < 5, a)
    print(list(b))
