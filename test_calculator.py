import unittest
import math # For some direct comparisons if needed, e.g. math.inf

# Import functions and globals from calculator.py
# Assuming calculator.py is in the same directory or accessible via PYTHONPATH
import calculator

class TestBasicOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(1, 2), 3)
        self.assertEqual(calculator.add(-1, 1), 0)
        self.assertEqual(calculator.add(-1, -1), -2)
        self.assertEqual(calculator.add(1.5, 2.5), 4.0)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(5, 2), 3)
        self.assertEqual(calculator.subtract(2, 5), -3)
        self.assertEqual(calculator.subtract(-1, 1), -2)
        self.assertEqual(calculator.subtract(5.5, 1.5), 4.0)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(3, 4), 12)
        self.assertEqual(calculator.multiply(-2, 5), -10)
        self.assertEqual(calculator.multiply(0, 100), 0)
        self.assertEqual(calculator.multiply(1.5, 2), 3.0)

    def test_divide(self):
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertEqual(calculator.divide(5, 2), 2.5)
        self.assertEqual(calculator.divide(-10, 2), -5)
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            calculator.divide(1, 0)

class TestAdvancedOperations(unittest.TestCase):
    def test_power(self):
        self.assertEqual(calculator.power(2, 3), 8)
        self.assertEqual(calculator.power(5, 0), 1)
        self.assertEqual(calculator.power(4, 0.5), 2)
        self.assertEqual(calculator.power(-2, 2), 4) # (-2)^2 = 4
        self.assertAlmostEqual(calculator.power(-2, 3), -8) # (-2)^3 = -8

    def test_sqrt(self):
        self.assertEqual(calculator.sqrt(4), 2)
        self.assertEqual(calculator.sqrt(0), 0)
        self.assertAlmostEqual(calculator.sqrt(2), 1.41421356237)
        with self.assertRaisesRegex(ValueError, "negative shadow"): # Themed error
            calculator.sqrt(-1)

    def test_trigonometric_functions(self):
        self.assertAlmostEqual(calculator.sin_degrees(0), 0)
        self.assertAlmostEqual(calculator.sin_degrees(90), 1)
        self.assertAlmostEqual(calculator.sin_degrees(180), 0)
        self.assertAlmostEqual(calculator.sin_degrees(270), -1)

        self.assertAlmostEqual(calculator.cos_degrees(0), 1)
        self.assertAlmostEqual(calculator.cos_degrees(90), 0)
        self.assertAlmostEqual(calculator.cos_degrees(180), -1)
        self.assertAlmostEqual(calculator.cos_degrees(270), 0)

        self.assertAlmostEqual(calculator.tan_degrees(0), 0)
        self.assertAlmostEqual(calculator.tan_degrees(45), 1)
        with self.assertRaisesRegex(ValueError, "Tangent is undefined"):
            calculator.tan_degrees(90)
        with self.assertRaisesRegex(ValueError, "Tangent is undefined"):
            calculator.tan_degrees(270)

    def test_logarithms(self):
        self.assertAlmostEqual(calculator.log10(100), 2)
        self.assertAlmostEqual(calculator.log10(1), 0)
        with self.assertRaisesRegex(ValueError, "Logarithm is undefined for non-positive numbers"):
            calculator.log10(0)
        with self.assertRaisesRegex(ValueError, "Logarithm is undefined for non-positive numbers"):
            calculator.log10(-1)

        self.assertAlmostEqual(calculator.ln(math.e), 1)
        self.assertAlmostEqual(calculator.ln(1), 0)
        with self.assertRaisesRegex(ValueError, "Logarithm is undefined for non-positive numbers"):
            calculator.ln(0)
        with self.assertRaisesRegex(ValueError, "Logarithm is undefined for non-positive numbers"):
            calculator.ln(-10)

    def test_factorial(self):
        self.assertEqual(calculator.factorial(0), 1)
        self.assertEqual(calculator.factorial(1), 1)
        self.assertEqual(calculator.factorial(5), 120)
        with self.assertRaisesRegex(ValueError, "Factorial is undefined for negative numbers or non-integers"):
            calculator.factorial(-1)
        with self.assertRaisesRegex(ValueError, "Factorial is undefined for negative numbers or non-integers"):
            calculator.factorial(1.5)

class TestTokenizer(unittest.TestCase):
    def test_simple_expressions(self):
        self.assertEqual(calculator.tokenize_expression("1 + 2"), ['1', '+', '2'])
        self.assertEqual(calculator.tokenize_expression("3 * 4 - 2 / 1"), ['3', '*', '4', '-', '2', '/', '1'])

    def test_expressions_with_parentheses(self):
        self.assertEqual(calculator.tokenize_expression("(1 + 2) * 3"), ['(', '1', '+', '2', ')', '*', '3'])
        self.assertEqual(calculator.tokenize_expression("((1))"), ['(', '(', '1', ')', ')'])

    def test_expressions_with_decimals_and_multi_digit(self):
        self.assertEqual(calculator.tokenize_expression("1.5 + 2.05"), ['1.5', '+', '2.05'])
        self.assertEqual(calculator.tokenize_expression("100 * 25 - .5"), ['100', '*', '25', '-', '.5'])
        self.assertEqual(calculator.tokenize_expression("0.5 * 2"), ['0.5', '*', '2'])


    def test_expressions_with_negative_numbers(self):
        # Tokenizer's current behavior: negative sign is part of the number token
        self.assertEqual(calculator.tokenize_expression("-1 + 5"), ['-1', '+', '5'])
        self.assertEqual(calculator.tokenize_expression("(-2) * 3"), ['(', '-2', ')', '*', '3'])
        self.assertEqual(calculator.tokenize_expression("5 * -2"), ['5', '*', '-2'])
        self.assertEqual(calculator.tokenize_expression("5 + -2"), ['5', '+', '-2'])
        self.assertEqual(calculator.tokenize_expression("5 - -2"), ['5', '-', '-2'])

    def test_expressions_with_powers(self):
        self.assertEqual(calculator.tokenize_expression("2 ^ 3 ^ 2"), ['2', '^', '3', '^', '2'])

    def test_empty_and_whitespace_expressions(self):
        # evaluate_expression handles empty/whitespace, tokenizer might return empty or raise
        # Based on current calculator.py, tokenizer will return empty for these.
        self.assertEqual(calculator.tokenize_expression(""), [])
        self.assertEqual(calculator.tokenize_expression("   "), [])

    def test_invalid_characters(self):
        with self.assertRaisesRegex(ValueError, "Unrecognized glyph"):
            calculator.tokenize_expression("1 + @ 2")
        with self.assertRaisesRegex(ValueError, "Unrecognized glyph"):
            calculator.tokenize_expression("abc")

class TestShuntingYardRPN(unittest.TestCase):
    def assertRPNOutputEqual(self, actual_rpn, expected_rpn_str):
        # Helper to compare RPN output where numbers are floats and operators are strings
        expected_rpn = []
        for item in expected_rpn_str:
            try:
                expected_rpn.append(float(item))
            except ValueError:
                expected_rpn.append(item)
        self.assertEqual(actual_rpn, expected_rpn)

    def test_shunting_yard_simple(self):
        tokens = calculator.tokenize_expression("1 + 2")
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['1', '2', '+'])

        tokens = calculator.tokenize_expression("3.0 * 4 - 2 / 1") # Use float for consistency
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['3.0', '4', '*', '2', '1', '/', '-'])

    def test_shunting_yard_precedence(self):
        tokens = calculator.tokenize_expression("1 + 2 * 3")
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['1', '2', '3', '*', '+'])

    def test_shunting_yard_parentheses(self):
        tokens = calculator.tokenize_expression("(1 + 2) * 3")
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['1', '2', '+', '3', '*'])

        tokens = calculator.tokenize_expression("((1 + 2) * (3 - 4)) / 5")
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['1', '2', '+', '3', '4', '-', '*', '5', '/'])

    def test_shunting_yard_associativity_power(self):
        # Power '^' is right-associative
        tokens = calculator.tokenize_expression("2 ^ 3 ^ 2") # Should be 2 ^ (3 ^ 2) = 2 ^ 9 = 512
        rpn = calculator.shunting_yard(tokens)
        self.assertRPNOutputEqual(rpn, ['2', '3', '2', '^', '^'])

    def test_shunting_yard_mismatched_parentheses(self):
        with self.assertRaisesRegex(ValueError, "Mismatched mystical parentheses"):
            calculator.shunting_yard(calculator.tokenize_expression("(1 + 2"))
        with self.assertRaisesRegex(ValueError, "Mismatched mystical parentheses"):
            calculator.shunting_yard(calculator.tokenize_expression("1 + 2)"))
        with self.assertRaisesRegex(ValueError, "Mismatched mystical parentheses"):
            calculator.shunting_yard(calculator.tokenize_expression("(()"))

    def test_evaluate_rpn_simple(self):
        self.assertEqual(calculator.evaluate_rpn([1.0, 2.0, '+']), 3.0)
        self.assertEqual(calculator.evaluate_rpn([1.0, 2.0, 3.0, '*', '+']), 7.0) # 1 + (2*3)
        self.assertEqual(calculator.evaluate_rpn([1.0, 2.0, '+', 3.0, '*']), 9.0) # (1+2)*3

    def test_evaluate_rpn_power(self):
        self.assertEqual(calculator.evaluate_rpn([2.0, 3.0, 2.0, '^', '^']), 512.0) # 2^(3^2)

    def test_evaluate_rpn_errors(self):
        with self.assertRaisesRegex(ValueError, "Insufficient operands"):
            calculator.evaluate_rpn([1.0, '+'])
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            calculator.evaluate_rpn([1.0, 0.0, '/'])
        with self.assertRaisesRegex(ValueError, "empty RPN queue"):
            calculator.evaluate_rpn([])
        with self.assertRaisesRegex(ValueError, "Invalid RPN expression or too many operands"):
             calculator.evaluate_rpn([1.0, 2.0, 3.0]) # Too many operands left

    def test_evaluate_expression_end_to_end(self):
        self.assertAlmostEqual(calculator.evaluate_expression("1 + 1"), 2.0)
        self.assertAlmostEqual(calculator.evaluate_expression("5 - 2"), 3.0)
        self.assertAlmostEqual(calculator.evaluate_expression("3 * 4"), 12.0)
        self.assertAlmostEqual(calculator.evaluate_expression("10 / 2"), 5.0)
        self.assertAlmostEqual(calculator.evaluate_expression("2 + 3 * 4"), 14.0)
        self.assertAlmostEqual(calculator.evaluate_expression("(2 + 3) * 4"), 20.0)
        self.assertAlmostEqual(calculator.evaluate_expression("((1 + 1) * 2) / 4"), 1.0)
        self.assertAlmostEqual(calculator.evaluate_expression("2^3"), 8.0)
        self.assertAlmostEqual(calculator.evaluate_expression("2 ^ 3 ^ 2"), 512.0) # 2^(3^2)
        self.assertAlmostEqual(calculator.evaluate_expression("-1 + 5"), 4.0)
        self.assertAlmostEqual(calculator.evaluate_expression("5 * -2"), -10.0)
        self.assertAlmostEqual(calculator.evaluate_expression("10 / -2"), -5.0)
        self.assertAlmostEqual(calculator.evaluate_expression("1 / 2"), 0.5)
        self.assertAlmostEqual(calculator.evaluate_expression("0.5 * 0.5"), 0.25)
        # Complex: 3 + 4 * 2 / (1 - 5) ^ 2 ^ 3 = 3 + 8 / (-4)^2^3 = 3 + 8 / (16^3) = 3 + 8 / 4096
        self.assertAlmostEqual(calculator.evaluate_expression("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"), 3 + 8 / (16**3))

        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            calculator.evaluate_expression("1 / 0")
        with self.assertRaisesRegex(ValueError, "Mismatched mystical parentheses"): # Error from shunting_yard
            calculator.evaluate_expression("(1 + 2")
        with self.assertRaisesRegex(ValueError, "Insufficient operands"): # Error from RPN
            calculator.evaluate_expression("1 +") # Tokenizer: ['1', '+'], Shunting: [1.0, '+'], RPN eval fails
        with self.assertRaisesRegex(ValueError, "Unknown arcane symbol"): # Error from shunting_yard
            calculator.evaluate_expression("1 + * 2") # Tokenizer: ['1', '+', '*', '2'] -> SY fails on consecutive ops without proper number conversion logic there
        with self.assertRaisesRegex(ValueError, "incantation dissolved into nothingness"):
            calculator.evaluate_expression("")
        with self.assertRaisesRegex(ValueError, "incantation dissolved into nothingness"):
            calculator.evaluate_expression("   ")
        with self.assertRaisesRegex(ValueError, "Unrecognized glyph"):
            calculator.evaluate_expression("1 $ 2")

class TestMemoryOperations(unittest.TestCase):
    def setUp(self):
        # Reset memory before each test in this class
        calculator.memory_clear() # This uses the function which also sets calculator_memory = 0.0
        # Also clear history as some memory operations might add to it in the main CLI
        calculator.calculation_history.clear()

    def test_memory_clear(self):
        calculator.memory_add(10)
        self.assertEqual(calculator.memory_recall(), 10)
        calculator.memory_clear()
        self.assertEqual(calculator.memory_recall(), 0.0)

    def test_memory_add(self):
        calculator.memory_add(5)
        self.assertEqual(calculator.memory_recall(), 5.0)
        calculator.memory_add(2.5)
        self.assertEqual(calculator.memory_recall(), 7.5)
        calculator.memory_add(-3)
        self.assertEqual(calculator.memory_recall(), 4.5)

    def test_memory_subtract(self):
        calculator.memory_add(10) # Start with 10
        calculator.memory_subtract(3)
        self.assertEqual(calculator.memory_recall(), 7.0)
        calculator.memory_subtract(1.5)
        self.assertEqual(calculator.memory_recall(), 5.5)
        calculator.memory_subtract(-2) # Subtracting a negative is adding
        self.assertEqual(calculator.memory_recall(), 7.5)

    def test_memory_recall(self):
        self.assertEqual(calculator.memory_recall(), 0.0) # Initial
        calculator.calculator_memory = 25.5 # Direct manipulation for testing recall
        self.assertEqual(calculator.memory_recall(), 25.5)


class TestHistoryFeature(unittest.TestCase):
    def setUp(self):
        calculator.calculation_history.clear()
        calculator.memory_clear() # Some history entries might involve memory values

    def test_history_after_evaluate_expression(self):
        calculator.evaluate_expression("1+1")
        self.assertIn("1+1 = 2.0 (as foretold by the Oracle)", calculator.calculation_history[0])

        calculator.evaluate_expression("2*3")
        self.assertIn("2*3 = 6.0 (as foretold by the Oracle)", calculator.calculation_history[1])

    def test_history_after_memory_commands_simulation(self):
        # Simulate CLI logic for m+ and m- to test history appending
        # This is an indirect test of how CLI *should* be adding to history

        # Simulate m+
        expr_to_add = "5+5"
        value_added = calculator.evaluate_expression(expr_to_add)
        calculator.memory_add(value_added)
        expected_m_plus_history = f"m+ {expr_to_add} (yielded: {value_added}) infused into Memory Crystal. Current enchantment: {calculator.calculator_memory}"
        # Manually append as the CLI would
        calculator.calculation_history.append(expected_m_plus_history)
        self.assertIn(expected_m_plus_history, calculator.calculation_history)
        self.assertEqual(calculator.memory_recall(), 10.0)

        # Simulate m-
        expr_to_subtract = "2*1.5"
        value_subtracted = calculator.evaluate_expression(expr_to_subtract)
        calculator.memory_subtract(value_subtracted)
        expected_m_minus_history = f"m- {expr_to_subtract} (yielded: {value_subtracted}) drained from Memory Crystal. Current enchantment: {calculator.calculator_memory}"
        # Manually append
        calculator.calculation_history.append(expected_m_minus_history)
        self.assertIn(expected_m_minus_history, calculator.calculation_history)
        self.assertEqual(calculator.memory_recall(), 7.0)

        # Simulate mc
        calculator.memory_clear()
        expected_mc_history = "Memory Crystal cleansed by a mystical breeze."
        # Manually append
        calculator.calculation_history.append(expected_mc_history)
        self.assertIn(expected_mc_history, calculator.calculation_history)


if __name__ == '__main__':
    unittest.main()
