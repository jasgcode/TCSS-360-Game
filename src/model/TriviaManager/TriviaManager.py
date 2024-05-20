import random

def load_questions():
    """
    Loads the trivia questions.
    Returns a list of Question objects.
    """
    # TODO: Implement the logic to load questions from a file or database
    # For simplicity, we'll use a hardcoded list of questions for demonstration purposes
    questions = [
        Question("What are the four main ingredients in beer?", ["Grain, hops, yeast, and water", "Grain, sugar, yeast, and water", "Hops, malt, yeast, and milk", "Grain, hops, yeast, and juice"], 0),
        Question("What drink uses Orange juice, Pineapple juice, Lime juice, Rum, and Grenadine?", ["Caribbean Rum", "Mojito", "Margarita", "Piña Colada"], 0),
        Question("Guinness beer was first brewed in which country?", ["Ireland", "Scotland", "England", "Germany"], 0),
        Question("What popular soda beverage was originally developed as a mixer for whiskey?", ["Mountain Dew", "Coca Cola", "Sprite", "Dr. Pepper"], 0),
        Question("To be legally sold as bourbon, a whiskey's mash must contain at least 51% of what grain?", ["Wheat", "Corn", "Rye", "Barley"], 1),
        Question("Champagne is a sparkling wine made from grapes grown in the Champagne region of which country?", ["France", "Italy", "Spain", "United States"], 0),
        Question("A Moscow Mule is a type of cocktail popularly served in what?", ["Copper Mug", "Martini Glass", "Highball Glass", "Shot Glass"], 0),
        Question("If a liquor is 100 proof how much alcohol does it contain by percentage?", ["50 Percent", "25 Percent", "75 Percent", "100 Percent"], 0),
        Question("What is the national drink of Mexico?", ["Tequila", "Mezcal", "Margarita", "Paloma"], 0),
        Question("What is the main ingredient in gin?", ["Juniper berries", "Vodka", "Whiskey", "Rum"], 0),
        # Add more questions here
    ]

    # Shuffle the answer choices for each question
    for question in questions:
        random.shuffle(question.choices)

    return questions


class TriviaManager:
    """
    The Trivia manager class for the Trivia Maze Game.
    Manages the trivia questions and handles the question selection
    """

    def __init__(self):
        """
        Initializes the trivia manager.
        """
        self.questions = load_questions()
        self.difficulty_level = None

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
