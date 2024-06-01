import sqlite3
import os


class Database:
    def __init__(self, db_name):
        # Get the directory path of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the relative path to the database file
        db_path = os.path.join(script_dir, db_name)

        # Connect to the database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_random_question(self, difficulty):
        self.cursor.execute('''
            SELECT question_text, answer_choices, correct_answer_index
            FROM questions
            WHERE difficulty = ?
            ORDER BY RANDOM()
            LIMIT 1
        ''', (difficulty,))

        result = self.cursor.fetchone()
        if result:
            question_text, answer_choices, correct_answer_index = result
            answer_choices = answer_choices.split('|')
            return question_text, answer_choices, correct_answer_index
        else:
            return None

    def close(self):
        self.conn.close()