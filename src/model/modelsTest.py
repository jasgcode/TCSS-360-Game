import unittest
from unittest.mock import MagicMock, patch
from GameModel import GameModel
from src.model.Entity.Player import Player
from src.model.Entity.Entity import Position

class TestGameModel(unittest.TestCase):
    def setUp(self):
        self.game_model = GameModel()

    def test_set_difficulty_level(self):
        self.game_model.set_difficulty_level("Easy")
        self.assertEqual(self.game_model.difficulty_level, "Easy")
        self.assertEqual(self.game_model.trivia_question_interval, 20)
        self.assertEqual(self.game_model.num_mobs, 5)
        self.assertEqual(self.game_model.cell_size, 28)
        self.assertEqual(self.game_model.lives, 5)

    @patch('GameModel.random.randrange')
    def test_mob_spawn(self, mock_randrange):
        mock_randrange.side_effect = [5, 5]
        maze = MagicMock()
        maze.width = 10
        maze.height = 10
        position = self.game_model.mob_spawn(maze)
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 5)

    def test_check_player_position_cell_value(self):
        self.game_model.maze = MagicMock()
        self.game_model.player = MagicMock()
        self.game_model.player.position.x = 3
        self.game_model.player.position.y = 3
        self.game_model.maze.maze = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0.75, 0], [0, 0, 0, 0, 0]]
        self.assertEqual(self.game_model.check_player_position_cell_value(), 0.75)

    def test_check_mob_encounter(self):
        self.game_model.mobs_positions = [Position(1, 1), Position(2, 2), Position(3, 3)]
        self.game_model.player = MagicMock()
        self.game_model.player.position = Position(2, 2)
        self.game_model.mobs = [MagicMock(), MagicMock(), MagicMock()]
        self.game_model.mobs[1].fight = True
        self.assertEqual(self.game_model.check_mob_encounter(), 1)

    def test_remove_mob(self):
        self.game_model.mobs = [MagicMock(), MagicMock(), MagicMock()]
        self.game_model.mobs_positions = [Position(1, 1), Position(2, 2), Position(3, 3)]
        self.game_model.remove_mob(1)
        self.assertEqual(len(self.game_model.mobs), 2)
        self.assertEqual(len(self.game_model.mobs_positions), 2)


    def test_should_ask_trivia_question(self):
        self.game_model.trivia_question_timer = 20
        self.game_model.trivia_question_interval = 20
        self.assertTrue(self.game_model.should_ask_trivia_question())

    def test_answer_trivia_question_correctly(self):
        self.game_model.score = 0
        self.game_model.trivia_question_timer = 10
        self.game_model.answer_trivia_question_correctly()
        self.assertEqual(self.game_model.score, 10)
        self.assertEqual(self.game_model.trivia_question_timer, 0)

    def test_answer_trivia_question_incorrectly(self):
        self.game_model.score = 10
        self.game_model.trivia_question_timer = 10
        self.game_model.lives = 3
        self.game_model.answer_trivia_question_incorrectly()
        self.assertEqual(self.game_model.score, 5)
        self.assertEqual(self.game_model.trivia_question_timer, 0)
        self.assertEqual(self.game_model.lives, 2)

if __name__ == '__main__':
    unittest.main()