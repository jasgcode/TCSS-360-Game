import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_random_question(self, difficulty):
        query = '''
            SELECT id, question_text, answer_choices, correct_answer_index
            FROM questions
            WHERE difficulty = ? AND has_been_shown = 0
            ORDER BY RANDOM()
            LIMIT 1
        '''
        self.cursor.execute(query, (difficulty,))

        result = self.cursor.fetchone()
        if result:
            question_id, question_text, answer_choices, correct_answer_index = result
            answer_choices = answer_choices.split('|')
            self.mark_question_as_shown(question_id)
            return question_text, answer_choices, correct_answer_index
        else:
            return None

    def mark_question_as_shown(self, question_id):
        query = '''
            UPDATE questions
            SET has_been_shown = 1
            WHERE id = ?
        '''
        self.cursor.execute(query, (question_id,))
        self.conn.commit()


    def close(self):
        self.conn.close()