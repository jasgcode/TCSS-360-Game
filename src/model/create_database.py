import sqlite3
# This script creates a SQLite database and populates it with some trivia questions.
def create_database():
    conn = sqlite3.connect('trivia.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            answer_choices TEXT NOT NULL,
            correct_answer_index INTEGER NOT NULL,
            difficulty TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

    #
def populate_database():
    questions = [
        {
            'question_text': 'What is the main ingredient in beer that gives it its alcohol content?',
            'answer_choices': 'Hops|Water|Yeast|Malt',
            'correct_answer_index': 2,
            'difficulty': 'easy'
        },
        {
            'question_text': 'Which country consumes the most beer per capita?',
            'answer_choices': 'USA|Germany|Czech Republic|Ireland',
            'correct_answer_index': 2,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the technical term for the fear of running out of beer?',
            'answer_choices': 'Humulonephobia|Zythophobia|Cenosillicaphobia|Lagerstalgia',
            'correct_answer_index': 2,
            'difficulty': 'hard'
        }
    ]

    conn = sqlite3.connect('trivia.db')
    cursor = conn.cursor()

    for question in questions:
        cursor.execute('''
            INSERT INTO questions (question_text, answer_choices, correct_answer_index, difficulty)
            VALUES (?, ?, ?, ?)
        ''', (
            question['question_text'],
            question['answer_choices'],
            question['correct_answer_index'],
            question['difficulty']
        ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    populate_database()
    print("Database created and populated successfully.")