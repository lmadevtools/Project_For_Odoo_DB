from config import DIR_LOGS_FILES
import unittest

#discover and run all files called test_xxxxx.py found in Tests --> this permits to add new files or test without update manually 
loader = unittest.TestLoader()
suite = loader.discover(start_dir="Tests", pattern="test_*.py")

'''
#display in the console -- replaced by the save into file run_tests.txt 
runner = unittest.TextTestRunner(verbosity=2) #verbosity = 2 to display detail of each test
result = runner.run(suite)
'''

# Open file for writing results
output_file = DIR_LOGS_FILES+"run_tests.txt"
with open(output_file, "w", encoding="utf-8") as f:
    runner = unittest.TextTestRunner(stream=f, verbosity=2)
    result = runner.run(suite)

#Display summary to console
print(f"Results written to: {output_file}")
print(f"Ran {result.testsRun} tests")
print(f"Failures: {len(result.failures)}")
print(f"Errors: {len(result.errors)}")
print("Success:", result.wasSuccessful())

'''
Sample of output :

test_negative_quantity_error (test_stock_move.TestStockMoveInit.test_negative_quantity_error) ... ERROR 
forced the error with an empty ID, and didn't catch the error.
def test_negative_quantity_error(self):
    m = StockMove("P1", "Laptop", 10, "in", "Restock")
    self.assertEqual(m.product_id,   )

test_negative_quantity_raise_error (test_stock_move.TestStockMoveInit.test_negative_quantity_raise_error) ... ok
'''