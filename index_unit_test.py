import unittest
from index import TaskManager, continuation_menu
from unittest.mock import patch
from io import StringIO

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        self.manager.add_task({'name': 'Task 1', 'priority': 3})
        self.assertEqual(len(self.manager.tasks), 1)

    def test_remove_existing_task(self):
        self.manager.add_task({'name': 'Task 1', 'priority': 3})
        result = self.manager.remove_task(0)
        self.assertEqual(result.valor, True)

    def test_remove_non_existing_task(self):
        result = self.manager.remove_task(0)
        self.assertEqual(result.valor, None)

    def test_list_tasks(self):
        self.manager.add_task({'name': 'Task 1', 'priority': 3})
        self.manager.add_task({'name': 'Task 2', 'priority': 1})
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_sort_tasks_by_priority(self):
        self.manager.add_task({'name': 'Task 1', 'priority': 3})
        self.manager.add_task({'name': 'Task 2', 'priority': 1})
        self.manager.sort_tasks_by_priority()
        self.assertEqual(self.manager.tasks[0]['priority'], 1)

class TestContinuationMenu(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_menu_display(self, mock_stdout):
        with patch('builtins.input', side_effect=['5']):
            continuation_menu(TaskManager())
            expected_output = "1. Add Task\n2. Remove Task\n3. List Tasks\n4. Sort Tasks by Priority\n5. Exit\nExiting...\n"
            actual_output = mock_stdout.getvalue().split("\n")[1:-1]  # Ignorando a linha em branco e "Exiting..."
            self.assertEqual(actual_output, expected_output.split("\n")[:-1])  # Ignorando "Exiting..." na saída esperada

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['1', 'Task 1', '3', '5'])
    def test_add_task(self, mock_input, mock_stdout):
        manager = TaskManager()
        continuation_menu(manager)
        self.assertEqual(len(manager.tasks), 1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['2', '0', '5'])
    def test_remove_existing_task(self, mock_input, mock_stdout):
        manager = TaskManager()
        manager.add_task({'name': 'Task 1', 'priority': 3})
        continuation_menu(manager)
        self.assertEqual(len(manager.tasks), 0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['2', '0', '5'])
    def test_remove_non_existing_task(self, mock_input, mock_stdout):
        manager = TaskManager()
        continuation_menu(manager)
        self.assertEqual(len(manager.tasks), 0)

if __name__ == '__main__':
    unittest.main()
