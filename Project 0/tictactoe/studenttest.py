import unittest
from tictactoe import *

class TestPlayerFunction(unittest.TestCase):
    def test_initial_state(self):
        board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), X)

    def test_x_turn(self):
        board = [[EMPTY, EMPTY, X],
                [X, O, O],
                [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), X)

    def test_o_turn(self):
        board = [[EMPTY, O, EMPTY],
                [EMPTY, EMPTY, X],
                [EMPTY, EMPTY, X]]
        self.assertEqual(player(board), O)

class TestActionsFunction(unittest.TestCase):
    def test_actions_partial_board(self):
        board = [[EMPTY, O, O],
                 [EMPTY, EMPTY, X],
                 [EMPTY, EMPTY, X]]
        expectedActions = {
            (0, 0), (1, 0), (1, 1), (2, 0), (2, 1)
        }
        self.assertEqual(actions(board), expectedActions)

    def test_actions_empty_board(self):
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        expectedActions = {
            (0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)
        }
        self.assertEqual(actions(board), expectedActions)

    def test_actions_full_board(self):
        board = [[X, O, O],
                 [O, O, X],
                 [X, X, X]]
        expectedActions = set()
        self.assertEqual(actions(board), expectedActions)

class TestResultsFunction(unittest.TestCase):
    def test_invalid_actions(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        with self.assertRaises(Exception, msg="Invalid action."): result(board, (0, 0))

    def test_valid_action(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        updatedBoard = [[X, O, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(result(board, (0, 1)), updatedBoard)

    def test_original_board_unchanged(self):
        board = initial_state()
        result(board, (0, 1))
        self.assertEqual(board, initial_state())

class TestWinnerFunction(unittest.TestCase):
    def test_row_win(self):
        board = [[X, X, X],
                 [EMPTY, O, EMPTY],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)

    def test_col_win(self):
        board = [[EMPTY, EMPTY, O],
                 [EMPTY, X, O],
                 [EMPTY, X, O]]
        self.assertEqual(winner(board), O)

    def test_diag_win(self):
        board = [[X, EMPTY, O],
                 [EMPTY, X, EMPTY],
                 [O, EMPTY, X]]
        self.assertEqual(winner(board), X)

    def test_empty_win(self):
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertIsNone(winner(board))

    def test_no_win(self):
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertIsNone(winner(board))

class TestTerminalFunction(unittest.TestCase):
    def test_game_won(self):
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertTrue(terminal(board))

    def test_game_draw(self):
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertTrue(terminal(board))

    def test_game_unfinished(self):
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, EMPTY]]
        self.assertFalse(terminal(board))

    def test_empty_board(self):
        board = initial_state()
        self.assertFalse(terminal(board))

class TestUtilityFunction(unittest.TestCase):
    def test_game_X_win(self):
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertEqual(utility(board), 1)

    def test_game_O_win(self):
        board = [[O, O, X],
                 [X, O, X],
                 [X, X, O]]
        self.assertEqual(utility(board), -1)

    def test_game_draw(self):
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertEqual(utility(board), 0)

    def test_game_empty(self):
        board = initial_state()
        self.assertEqual(utility(board), 0)

class TestMiniMaxFunction(unittest.TestCase):
    def test_optimal_move_X(self):
        board = [[X, O, X],
                 [O, X, EMPTY],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (2, 2))

    def test_optimal_move_O(self):
        board = [[X, O, X],
                 [EMPTY, X, EMPTY],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (2, 2))

    def test_draw_scenario(self):
        board = [[X, O, X],
                 [X, X, O],
                 [O, X, O]]
        self.assertIsNone(minimax(board))

    def test_terminal_state(self):
        board = [[X, X, X],
                 [EMPTY, EMPTY, O],
                 [EMPTY, O, EMPTY]]
        self.assertIsNone(minimax(board))

if __name__ == "__main__":
    unittest.main()