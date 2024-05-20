import pygame


class TriviaQuestion:
    """
    TriviaQuestion is a class that represents a trivia question.
    """
    def __init__(self, question, choices, correct_answer, difficulty):
        """
        Initializes a TriviaQuestion object i.e. a question and a list of choices.

        """
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.answered = False
        self.timer = 0
        self.max_time = 30  # Maximum time to answer the question (in seconds)

    def display(self, screen, font, x, y):
        """

        """
        question_text = font.render(self.question, True, (255, 255, 255))
        screen.blit(question_text, (x, y))

        for i, choice in enumerate(self.choices):
            choice_text = font.render(f"{chr(ord('A') + i)}. {choice}", True, (255, 255, 255))
            screen.blit(choice_text, (x, y + 30 + i * 30))

    def update(self, dt):
        """
        Updates the timer for the TriviaQuestion
        """
        if not self.answered:
            self.timer += dt
            if self.timer >= self.max_time:
                self.answered = True
                return False
        return True

    def check_answer(self, player_answer):
        """
        Checks if the player answer is correct.
        """
        if not self.answered:
            self.answered = True
            return player_answer == self.correct_answer
        return False
