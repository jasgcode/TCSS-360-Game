import sqlite3

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

def populate_database():
    questions = [
        {
            'question_text': 'What is the capital of France?',
            'answer_choices': 'London|Paris|Berlin|Madrid',
            'correct_answer_index': 1,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the largest planet in our solar system?',
            'answer_choices': 'Mars|Jupiter|Saturn|Neptune',
            'correct_answer_index': 1,
            'difficulty': 'medium'
        },
        {
            'question_text': 'Who painted the Mona Lisa?',
            'answer_choices': 'Leonardo da Vinci|Vincent van Gogh|Pablo Picasso|Michelangelo',
            'correct_answer_index': 0,
            'difficulty': 'easy'
        },
        # Add more questions here
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