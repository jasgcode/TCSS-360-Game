class TriviaQuestion:
    def __init__(self, question_text, answer_choices, correct_answer_index):
        """
        Initialize the TriviaQuestion with question text, answer choices, and the correct answer index.
        """

        self.question_text = question_text
        self.answer_choices = answer_choices
        self.correct_answer_index = correct_answer_index
