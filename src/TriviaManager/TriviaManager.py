import random

class TriviaManager:
    """
    Trivia manager class for the Python Trivia Maze Game.
    Manages the trivia questions and handles the question selection and answer verification.
    """

    def __init__(self):
        """
        Initializes the trivia manager.
        Loads the trivia questions from a file or database.
        """
        self.questions = self.load_questions()
        self.difficulty_level = None

    def load_questions(self):
        """
        Loads the trivia questions from a file or database.
        Returns a list of Question objects.
        """
        # TODO: Implement the logic to load questions from a file or database
        # For simplicity, we'll use a hardcoded list of questions for demonstration purposes
        questions = [
            Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 1),
            Question("What is the largest planet in our solar system?", ["Jupiter", "Saturn", "Neptune", "Uranus"], 1),
            Question("What is the currency of Japan?", ["Yen", "Dollar", "Euro", "Pound"], 1),
            # Add more questions here
        ]
        return questions

    def set_difficulty_level(self, difficulty_level):
        """
        Sets the difficulty level for the trivia questions.
        Filters the questions based on the difficulty level.
        """
        self.difficulty_level = difficulty_level
        if difficulty_level == "Easy":
            self.questions = [q for q in self.questions if q.difficulty == 1]
        elif difficulty_level == "Medium":
            self.questions = [q for q in self.questions if q.difficulty == 2]
        else:  # "Hard"
            self.questions = [q for q in self.questions if q.difficulty == 3]

    def get_random_question(self):
        """
        Retrieves a random question from the list of available questions.
        Returns a Question object.
        """
        return random.choice(self.questions)

    def is_answer_correct(self, question, user_answer):
        """
        Checks if the user's answer to a question is correct.
        Returns True if the answer is correct, False otherwise.
        """
        return question.correct_answer == user_answer