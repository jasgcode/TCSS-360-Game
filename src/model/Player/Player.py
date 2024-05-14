class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Player:
    def __init__(self, position, lives, score):
        self.position = position
        self.lives = lives
        self.score = score

    def move(self, direction):
        # Update the player's position based on the given direction
        if direction == "up":
            self.position.y -= 1
        elif direction == "down":
            self.position.y += 1
        elif direction == "left":
            self.position.x -= 1
        elif direction == "right":
            self.position.x += 1

    def answerQuestion(self, answer, question):
        if answer == question.getCorrectAnswer():
            self.score += 1
            print("Correct answer! Score:", self.score)
            return True
        else:
            self.lives -= 1
            print("Wrong answer! Lives remaining:", self.lives)
            return False

    def getPosition(self):
        return self.position

    def getLives(self):
        return self.lives

    def getScore(self):
        return self.score