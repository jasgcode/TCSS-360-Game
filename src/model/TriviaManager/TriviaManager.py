from src.model.data.database import Database

from src.model.TriviaQuestion.TriviaQuestion import TriviaQuestion


class TriviaManager:
    def __init__(self, difficulty_level):
        self.database = Database('trivia.db')
        self.difficulty_level = difficulty_level

    def get_trivia_question(self):
        question_data = self.database.get_random_question(self.difficulty_level)
        if question_data:
            question_text, answer_choices, correct_answer_index = question_data
            return TriviaQuestion(question_text, answer_choices, correct_answer_index)
        else:
            return None

    def close_database(self):
        self.database.close()
