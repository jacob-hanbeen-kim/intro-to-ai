import unittest
from tictactoe import *

class TestPlayerFunction(unittest.TestCase):
    def test_initial_state(self):
        board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(player(board), X, "X should play first in the initial state")

    def test_x_turn(self):
        board = [
            [X, O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(player(board), X, "It should be X's turn when X and O have equal moves")

    def test_o_turn(self):
        board = [
            [X, O, X],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(player(board), O, "It should be O's turn when X has one more move than O")

class TestActionsFunction(unittest.TestCase):
    def test_empty_board(self):
        board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        expected_actions = {
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        }
        self.assertEqual(actions(board), expected_actions, "All cells should be available on an empty board")

    def test_partial_board(self):
        board = [
            [X, O, EMPTY],
            [EMPTY, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        expected_actions = {
            (0, 2), (1, 0), (1, 2),
            (2, 1), (2, 2)
        }
        self.assertEqual(actions(board), expected_actions, "Should return only the empty cells")

    def test_full_board(self):
        board = [
            [X, O, X],
            [O, X, O],
            [X, O, X]
        ]
        expected_actions = set()  # No moves available
        self.assertEqual(actions(board), expected_actions, "No actions should be available on a full board")

class TestResultFunction(unittest.TestCase):
    def test_valid_action(self):
        board = initial_state()
        action = (0, 0)
        expected_board = [
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(result(board, action), expected_board, "The board should reflect the valid action")

    def test_invalid_action(self):
        board = [
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        action = (0, 0)  # Cell already occupied
        with self.assertRaises(Exception, msg="Invalid action"):
            result(board, action)

    def test_original_board_unchanged(self):
        board = initial_state()
        action = (0, 0)
        result(board, action)
        self.assertEqual(board, initial_state(), "The original board should not be modified")

class TestWinnerFunction(unittest.TestCase):
    def test_row_win(self):
        board = [
            [X, X, X],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(winner(board), X, "X should win with a complete row")

    def test_column_win(self):
        board = [
            [EMPTY, O, X],
            [EMPTY, O, X],
            [EMPTY, O, EMPTY]
        ]
        self.assertEqual(winner(board), O, "X should win with a complete column")

    def test_diagonal_win(self):
        board = [
            [X, O, EMPTY],
            [O, X, EMPTY],
            [EMPTY, EMPTY, X]
        ]
        self.assertEqual(winner(board), X, "X should win with a diagonal")

    def test_no_winner(self):
        board = [
            [X, O, X],
            [O, X, O],
            [O, X, O]
        ]
        self.assertIsNone(winner(board), "There should be no winner in a draw")

    def test_empty_board(self):
        board = initial_state()
        self.assertIsNone(winner(board), "There should be no winner on an empty board")

class TestTerminalFunction(unittest.TestCase):
    def test_game_won(self):
        board = [
            [X, X, X],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertTrue(terminal(board), "The game should be over when there is a winner")

    def test_game_draw(self):
        board = [
            [X, O, X],
            [O, X, O],
            [O, X, O]
        ]
        self.assertTrue(terminal(board), "The game should be over when there is a draw")

    def test_game_ongoing(self):
        board = [
            [X, O, EMPTY],
            [EMPTY, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        self.assertFalse(terminal(board), "The game should not be over when there are still possible moves")

    def test_empty_board(self):
        board = initial_state()
        self.assertFalse(terminal(board), "The game should not be over on an empty board")

class TestUtilityFunction(unittest.TestCase):
    def test_x_wins(self):
        board = [
            [X, X, X],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertEqual(utility(board), 1, "Utility should return 1 when X wins")

    def test_o_wins(self):
        board = [
            [O, X, X],
            [O, EMPTY, X],
            [O, EMPTY, EMPTY]
        ]
        self.assertEqual(utility(board), -1, "Utility should return -1 when O wins")

    def test_draw(self):
        board = [
            [X, O, X],
            [O, X, O],
            [O, X, O]
        ]
        self.assertEqual(utility(board), 0, "Utility should return 0 for a draw")

    def test_no_winner(self):
        board = [
            [X, O, EMPTY],
            [EMPTY, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        self.assertEqual(utility(board), 0, "Utility should return 0 when there is no winner")

class TestMinimaxFunction(unittest.TestCase):
    def test_optimal_move_x(self):
        board = [
            [X, O, X],
            [O, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        self.assertEqual(minimax(board), (2, 2), "X should choose the winning move (1, 2)")

    def test_optimal_move_o(self):
        board = [
            [X, O, X],
            [EMPTY, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        self.assertEqual(minimax(board), (2, 2), "O should block X's winning move at (2, 0)")

    def test_draw_scenario(self):
        board = [
            [X, O, X],
            [X, O, O],
            [O, X, X]
        ]
        self.assertIsNone(minimax(board), "Minimax should return None for a terminal board")

    def test_terminal_state(self):
        board = [
            [X, X, X],
            [O, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        self.assertIsNone(minimax(board), "Minimax should return None for a terminal board")

if __name__ == "__main__":
    unittest.main()