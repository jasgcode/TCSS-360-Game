from src.model.data.database import Database

from src.model.TriviaQuestion.TriviaQuestion import TriviaQuestion


class TriviaManager:
    def __init__(self, difficulty_level):
        """
        Initialize the TriviaManager with the specified difficulty level.
        """
        self.database = Database('trivia.db')
        self.difficulty_level = difficulty_level

    def get_trivia_question(self):
        """
        Retrieve a random trivia question based on the difficulty level.
        """
        question_data = self.database.get_random_question(self.difficulty_level)
        if question_data:
            question_text, answer_choices, correct_answer_index = question_data
            return TriviaQuestion(question_text, answer_choices, correct_answer_index)
        else:
            return None

    def close_database(self):
        """
        Close the connection to the trivia database.
        """

        self.database.close()
