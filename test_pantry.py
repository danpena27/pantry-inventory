import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pantry_classes import PantryItem, PantryManager


class PantryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'pantry.csv'
        self.manager = PantryManager(self.path)

    def call(self, function, answers=()):
        output = io.StringIO()
        with patch('builtins.input', side_effect=answers), redirect_stdout(output):
            function()
        return output.getvalue()

    def test_csv_round_trip_and_blank_lines(self):
        item = PantryItem('Beans', 'Canned Goods', 4, 1.25,
                          'Low sodium, "large" can\nSecond line', '09/30/2028')
        item.entry_date = '09/30/2026'
        self.manager.items.append(item)
        self.call(self.manager.save_data)
        with self.path.open('a', encoding='utf-8') as file:
            file.write('\n')
        restored = PantryManager(self.path)
        self.call(restored.load_data)
        self.call(restored.load_data)
        self.assertEqual(len(restored.items), 1)
        self.assertEqual(vars(restored.items[0]), vars(item))
        self.assertIn('Canned Goods', restored.categories)

    def test_missing_file(self):
        output = self.call(self.manager.load_data)
        self.assertIn('starting a new one', output)
        self.assertEqual(self.manager.items, [])

    def test_delete_later_item_and_missing_item(self):
        self.manager.items = [PantryItem(name, 'Grains', 1, 2, '', '')
                              for name in ['Rice', 'Oats']]
        output = self.call(self.manager.delete_item, ['Oats'])
        self.assertNotIn('not found', output)
        self.assertEqual([item.name for item in self.manager.items], ['Rice'])
        output = self.call(self.manager.delete_item, ['missing'])
        self.assertEqual(output.count('Item not found.'), 1)
        self.manager.items.clear()
        self.assertIn('Item not found.', self.call(self.manager.delete_item, ['missing']))

    def test_quantity_and_cost_validation(self):
        answers = ['Rice', 'Grains', 'Sample', '09/30/2027',
                   'bad', '-1', '0', '2', 'bad', '-1', 'nan', 'inf', '3.50']
        self.call(self.manager.add_item, answers)
        item = self.manager.items[0]
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.cost, 3.5)

    def test_partial_deletion(self):
        self.manager.items = [PantryItem('Rice', 'Grains', 4, 3.5, '', '')]
        self.call(self.manager.delete_item, ['Rice', '2'])
        self.assertEqual(self.manager.items[0].quantity, 2)

    def test_month_report_value(self):
        item = PantryItem('Rice', 'Grains', 2, 3.5, '', '')
        item.entry_date = '09/30/2026'
        self.manager.items = [item]
        output = self.call(self.manager.view_by_month, ['9'])
        self.assertIn('Current inventory value:$7.00', output)


if __name__ == '__main__':
    unittest.main()
