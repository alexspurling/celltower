import unittest
from celltower import next_letter_positions


class CellTowerTest(unittest.TestCase):
    def test_letter_positions(self):
        positions = [(0, 0), (1, 0), (2, 0)]
        next_positions = next_letter_positions(positions)
        self.assertEqual([(0, 1), (1, 1), (3, 0), (2, 1)], next_positions)

        positions = [(0, 0), (1, 0), (2, 0), (1, 1)]
        next_positions = next_letter_positions(positions)
        self.assertEqual([(3, 0), (2, 1), (1, 2)], next_positions)

        positions = [(0, 0), (1, 0), (2, 0), (1, 1)]
        next_positions = next_letter_positions(positions)
        self.assertEqual([(3, 0), (2, 1), (1, 2)], next_positions)



if __name__ == '__main__':
    unittest.main()
