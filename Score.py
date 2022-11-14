
class Score:
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