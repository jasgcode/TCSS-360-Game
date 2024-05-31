import sqlite3


# This script creates a SQLite database and populates it with trivia questions.
def create_database():
    conn = sqlite3.connect('data/trivia.db')
    cursor = conn.cursor()

    # Check if the questions table exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='questions'
    ''')
    table_exists = cursor.fetchone()

    if table_exists:
        # Check if the has_been_shown column exists
        cursor.execute('''
            PRAGMA table_info(questions)
        ''')
        columns = cursor.fetchall()
        has_been_shown_exists = any(column[1] == 'has_been_shown' for column in columns)

        if not has_been_shown_exists:
            # Add the has_been_shown column if it doesn't exist
            cursor.execute('''
                ALTER TABLE questions
                ADD COLUMN has_been_shown INTEGER DEFAULT 0
            ''')
    else:
        # Create the questions table with the has_been_shown column
        cursor.execute('''
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                answer_choices TEXT NOT NULL,
                correct_answer_index INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                has_been_shown INTEGER DEFAULT 0
            )
        ''')

    conn.commit()
    conn.close()

def populate_database():
    questions = [
        {
            'question_text': 'What is the main ingredient in beer that gives it its color?',
            'answer_choices': 'Hops|Water|Yeast|Malt',
            'correct_answer_index': 0,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the most common type of beer?',
            'answer_choices': 'Ale|Lager|Stout|Porter',
            'correct_answer_index': 1,
            'difficulty': 'easy'
        },
        {
            'question_text': 'Which country is known for its Oktoberfest celebration?',
            'answer_choices': 'USA|Germany|Czech Republic|Ireland',
            'correct_answer_index': 1,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the main difference between an ale and a lager?',
            'answer_choices': 'Color|Alcohol content|Fermentation process|Taste',
            'correct_answer_index': 2,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the most common glassware used for serving beer?',
            'answer_choices': 'Pint glass|Stein|Goblet|Mug',
            'correct_answer_index': 0,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the process of adding hops to beer called?',
            'answer_choices': 'Mashing|Boiling|Hopping|Fermenting',
            'correct_answer_index': 2,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the typical alcohol content of a light beer?',
            'answer_choices': '2-4%|4-6%|6-8%|8-10%',
            'correct_answer_index': 0,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the purpose of adding yeast to beer?',
            'answer_choices': 'To add flavor|To add color|To create alcohol|To create carbonation',
            'correct_answer_index': 2,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the most popular beer brand in the world?',
            'answer_choices': 'Budweiser|Heineken|Corona|Snow',
            'correct_answer_index': 3,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the term for a beer that is served from a keg?',
            'answer_choices': 'Bottled beer|Canned beer|Draft beer|Craft beer',
            'correct_answer_index': 2,
            'difficulty': 'easy'
        },
        {
            'question_text': 'What is the process of soaking grains in water to extract sugars called?',
            'answer_choices': 'Mashing|Boiling|Hopping|Fermenting',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the style of beer that originated in India?',
            'answer_choices': 'India Pale Ale|Stout|Porter|Hefeweizen',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the most expensive beer in the world?',
            'answer_choices': 'Nail Brewing Antarctic Nail Ale|BrewDog End of History|Schorschbräu Schorschbock 57|Samuel Adams Utopias',
            'correct_answer_index': 1,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the style of beer that is fermented with wild yeast?',
            'answer_choices': 'Lambic|Pilsner|Kölsch|Bock',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the country with the most breweries per capita?',
            'answer_choices': 'USA|Germany|Belgium|Czech Republic',
            'correct_answer_index': 2,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the term for a beer that is aged in wooden barrels?',
            'answer_choices': 'Barrel-aged|Cask-conditioned|Bottle-conditioned|Dry-hopped',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the style of beer that is known for its sour taste?',
            'answer_choices': 'Gose|Hefeweizen|Saison|Witbier',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the most awarded brewery in the world?',
            'answer_choices': 'Anheuser-Busch|BrewDog|Sierra Nevada|Weihenstephan',
            'correct_answer_index': 3,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with fruit?',
            'answer_choices': 'Fruit beer|Sour beer|Spice beer|Smoke beer',
            'correct_answer_index': 0,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the country that consumes the most beer in total?',
            'answer_choices': 'USA|China|Brazil|Russia',
            'correct_answer_index': 1,
            'difficulty': 'medium'
        },
        {
            'question_text': 'What is the style of beer that is known for its smoky flavor?',
            'answer_choices': 'Rauchbier|Schwarzbier|Dunkelweizen|Altbier',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with wild bacteria?',
            'answer_choices': 'Wild ale|Sour ale|Brett beer|Lambic',
            'correct_answer_index': 2,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the style of beer that is brewed with oysters?',
            'answer_choices': 'Oyster stout|Oyster porter|Oyster IPA|Oyster lager',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with coffee?',
            'answer_choices': 'Coffee stout|Espresso porter|Mocha IPA|Java lager',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the style of beer that is brewed with seaweed?',
            'answer_choices': 'Seaweed ale|Kelp lager|Algae stout|Nori porter',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with chili peppers?',
            'answer_choices': 'Chili beer|Pepper ale|Jalapeño lager|Habanero stout',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the style of beer that is brewed with squid ink?',
            'answer_choices': 'Squid ink stout|Cuttlefish porter|Octopus IPA|Nautilus lager',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with ghost peppers?',
            'answer_choices': 'Ghost pepper ale|Bhut jolokia lager|Carolina reaper stout|Trinidad scorpion porter',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the style of beer that is brewed with wasabi?',
            'answer_choices': 'Wasabi ale|Horseradish lager|Mustard stout|Ginger porter',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        },
        {
            'question_text': 'What is the term for a beer that is brewed with edible gold?',
            'answer_choices': 'Gold beer|Platinum ale|Silver lager|Diamond stout',
            'correct_answer_index': 0,
            'difficulty': 'hard'
        }
    ]

    conn = sqlite3.connect('data/trivia.db')
    cursor = conn.cursor()
    for question in questions:
        cursor.execute('''
                INSERT INTO questions (question_text, answer_choices, correct_answer_index, difficulty, has_been_shown)
                VALUES (?, ?, ?, ?, 0)
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
