import math
import re
import random # Added for fantasy theme

# --- Global Scope Variables ---
calculator_memory = 0.0
calculation_history = []

# A list of whimsical prefixes for error messages, adding to the calculator's unique theme.
FANTASY_ERROR_PREFIXES = [
    "Merlin's beard! The numbers rebelled!",
    "A mischievous gremlin has tangled your input!",
    "The calculation spirits are puzzled by that incantation.",
    "Hark! Your expression is as baffling as a dragon's riddle!",
    "Alas, the ancient runes of your expression are unreadable!"
]

# Defines the recognized operators, their precedence, and associativity.
# Precedence: Higher numbers indicate higher precedence.
# Associativity: 'L' for left-associative, 'R' for right-associative.
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'L'},
    '-': {'precedence': 1, 'associativity': 'L'},
    '*': {'precedence': 2, 'associativity': 'L'},
    '/': {'precedence': 2, 'associativity': 'L'},
    '^': {'precedence': 3, 'associativity': 'R'} # Exponentiation is typically right-associative
}

# --- Memory Functions ---
def memory_add(value):
  """Adds a value to the calculator memory."""
  global calculator_memory
  calculator_memory += value

def memory_subtract(value):
  """Subtracts a value from the calculator memory."""
  global calculator_memory
  calculator_memory -= value

def memory_recall():
  """Returns the current value of the calculator memory."""
  global calculator_memory
  return calculator_memory

def memory_clear():
  """Resets the calculator memory to 0.0."""
  global calculator_memory
  calculator_memory = 0.0

# --- Core Calculation Functions ---
def add(a, b):
  """Calculates the sum of two numbers."""
  return a + b

def subtract(a, b):
  """Calculates the difference of two numbers."""
  return a - b

def multiply(a, b):
  """Calculates the product of two numbers."""
  return a * b

def divide(a, b):
  """Calculates the division of a by b. Raises ValueError if b is zero."""
  if b == 0:
    # This themed error is raised if division by zero is attempted.
    raise ValueError("Cannot divide by zero (lest you tear the fabric of mathematics!)")
  return a / b

def power(base, exponent):
  """Calculates base raised to the power of exponent."""
  return math.pow(base, exponent)

# --- Advanced Calculation Functions ---
# These are not currently parsed by evaluate_expression (e.g., "sqrt(16)" in an expression string)
# but are kept for potential future use or if specific commands for them were to be re-added.
def sqrt(number):
  """Calculates the square root of a number. Raises ValueError if number is negative."""
  if number < 0:
    raise ValueError("Cannot summon the square root of a negative shadow!")
  return math.sqrt(number)

# ... (other advanced functions like sin, cos, etc., can be themed if re-enabled)
# Their docstrings are standard and clear.

# --- Expression Evaluation Functions ---

def tokenize_expression(expression_string):
  """
  Converts an infix mathematical expression string into a list of tokens.

  Args:
    expression_string: The string representation of the infix expression.
                       It handles numbers (integers, decimals, optionally negative),
                       operators (+, -, *, /, ^), and parentheses ((, )).
                       Whitespace is ignored.

  Returns:
    A list of string tokens. For example, "1 + 2.5" -> ['1', '+', '2.5'].

  Raises:
    ValueError: If the expression string is None or contains unrecognized characters.
  """
  if expression_string is None:
    raise ValueError("A null incantation? The spirits are confused.")

  # Regex to identify numbers (including negatives at the start or after operators/parentheses),
  # operators, parentheses, and whitespace.
  token_pattern = re.compile(r"""
      (?P<NUMBER>   -?\d+\.\d*   | -?\d+\.?   )  # Numbers (integers or decimals, optionally negative)
    | (?P<OPERATOR>  [+\-*/^]      )  # Operators
    | (?P<LPAREN>    \(            )  # Left parenthesis
    | (?P<RPAREN>    \)            )  # Right parenthesis
    | (?P<WHITESPACE>\s+           )  # Whitespace (to be ignored)
    | (?P<MISMATCH>  .             )  # Any other character is a mismatch
  """, re.VERBOSE | re.IGNORECASE)

  tokens = []
  for match in token_pattern.finditer(expression_string):
    kind = match.lastgroup
    value = match.group()

    if kind == 'NUMBER':
      tokens.append(value)
    elif kind == 'OPERATOR':
      tokens.append(value)
    elif kind == 'LPAREN':
      tokens.append('(')
    elif kind == 'RPAREN':
      tokens.append(')')
    elif kind == 'WHITESPACE':
      continue # Ignore whitespace
    elif kind == 'MISMATCH':
      raise ValueError(f"An unrecognized glyph '{value}' appears in your spell!")
  return tokens


def shunting_yard(tokens):
  """
  Converts a list of infix tokens to Reverse Polish Notation (RPN) using the Shunting-Yard algorithm.

  Args:
    tokens: A list of string tokens (numbers, operators, parentheses) from tokenize_expression.

  Returns:
    A list representing the RPN queue, where numbers are floats and operators/parentheses are strings.

  Raises:
    ValueError: If parentheses are mismatched or an unknown token is encountered.
  """
  output_queue = []
  operator_stack = [] # Acts as the operator stack for the algorithm.

  for token_str in tokens:
    try:
      # Convert number tokens to float.
      num = float(token_str)
      output_queue.append(num)
    except ValueError: # Token is not a number, so it's an operator or parenthesis.
      token = token_str
      if token in OPERATORS:
        op1 = token
        # Shunting-Yard logic for operator precedence and associativity.
        while (operator_stack and
               operator_stack[-1] != '(' and
               (OPERATORS[operator_stack[-1]]['precedence'] > OPERATORS[op1]['precedence'] or
                (OPERATORS[operator_stack[-1]]['precedence'] == OPERATORS[op1]['precedence'] and
                 OPERATORS[op1]['associativity'] == 'L'))):
          output_queue.append(operator_stack.pop())
        operator_stack.append(op1)
      elif token == '(':
        operator_stack.append(token)
      elif token == ')':
        # Pop operators onto the output queue until a left parenthesis is found.
        while operator_stack and operator_stack[-1] != '(':
          output_queue.append(operator_stack.pop())
        if not operator_stack or operator_stack[-1] != '(': # Mismatched parenthesis check
          raise ValueError("Mismatched mystical parentheses! Check your (, ) seals.")
        operator_stack.pop() # Pop the '(' from the stack and discard.
      else:
        # This should ideally not be reached if tokenize_expression is robust.
        raise ValueError(f"Unknown arcane symbol '{token}' encountered during Shunting-Yard ritual.")

  # Pop any remaining operators from the stack to the output queue.
  while operator_stack:
    op = operator_stack.pop()
    if op == '(': # A leftover '(' indicates mismatched parentheses.
      raise ValueError("Mismatched mystical parentheses! An opening seal '(' was left unbound.")
    output_queue.append(op)

  return output_queue

def evaluate_rpn(rpn_queue):
  """
  Evaluates an expression provided in Reverse Polish Notation (RPN).

  Args:
    rpn_queue: A list of tokens (numbers as floats, operators as strings) in RPN.

  Returns:
    The numerical result of the expression.

  Raises:
    ValueError: For issues like insufficient operands for an operator,
                unknown operators, or an empty/invalid RPN queue.
  """
  operand_stack = [] # Stack to hold operands during RPN evaluation.
  for token in rpn_queue:
    if isinstance(token, float): # If the token is a number, push it onto the stack.
      operand_stack.append(token)
    elif token in OPERATORS: # If the token is an operator.
      if len(operand_stack) < 2: # Check for enough operands.
        raise ValueError(f"Not enough numbers on the sacred stack for operator '{token}'!")
      # Pop the top two operands from the stack.
      op2 = operand_stack.pop()
      op1 = operand_stack.pop()

      # Perform the operation based on the operator token.
      if token == '+': result = add(op1, op2)
      elif token == '-': result = subtract(op1, op2)
      elif token == '*': result = multiply(op1, op2)
      elif token == '/': result = divide(op1, op2) # `divide` handles its own zero-division error.
      elif token == '^': result = power(op1, op2)
      else:
        # This case should not be reached if OPERATORS keys are consistent.
        raise ValueError(f"Unknown operator '{token}' during RPN evaluation ritual.")
      operand_stack.append(result) # Push the result back onto the stack.
    else:
      # This case implies an unrecognized token in the RPN queue.
      raise ValueError(f"Mysterious token '{token}' found in RPN queue.")

  if len(operand_stack) == 1: # The final result should be the only item on the stack.
    return operand_stack[0]
  elif not operand_stack and not rpn_queue: # Original expression was empty or invalid.
    raise ValueError("Cannot evaluate an empty spell (empty RPN queue).")
  else:
    # If more or less than one item remains, the RPN expression was malformed.
    raise ValueError("The RPN spell left too many (or too few) numbers on the stack! Likely an invalid incantation.")


def evaluate_expression(expression_string):
  """
  Orchestrates the evaluation of a mathematical expression string.
  It tokenizes the string, converts it to RPN, and then evaluates the RPN queue.

  Args:
    expression_string: The infix mathematical expression as a string.

  Returns:
    The numerical result of the expression.

  Raises:
    ValueError: If any step (tokenization, Shunting-Yard, RPN evaluation) fails,
                or if the expression string itself is invalid (e.g., empty).
                The error message will be specific to the failure point.
  """
  if not expression_string or not expression_string.strip():
      raise ValueError("You must provide an incantation (expression) to evaluate!")
  try:
    # Step 1: Convert the expression string into a list of tokens.
    tokens = tokenize_expression(expression_string)
    if not tokens:
      # This can happen if the expression_string contains only whitespace, for example.
      raise ValueError("Your incantation dissolved into nothingness (no tokens found).")

    # Step 2: Convert the list of infix tokens to Reverse Polish Notation (RPN).
    rpn_queue = shunting_yard(tokens)
    # Note: An expression like "()" is valid syntax for shunting_yard and results in an empty rpn_queue.
    # evaluate_rpn will then correctly raise an error for an empty queue.

    # Step 3: Evaluate the RPN queue to get the final result.
    result = evaluate_rpn(rpn_queue)
    return result
  except ValueError as ve:
    # Re-raise ValueErrors from underlying functions to provide specific error context.
    raise ValueError(str(ve))
  except Exception as e:
    # Catch any other unexpected errors during the evaluation process.
    error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
    raise ValueError(f"{error_prefix} An unforeseen mystical disturbance occurred: {str(e)}")


# --- CLI Main Loop ---
# This section handles user interaction for the command-line interface.
if __name__ == "__main__":
  print("Greetings, Math Magician! The Great Calculator of Whimsy awaits your commands.")
  print("Type 'help' for a mystical guide, or 'vanish' to depart. Let the numbers dance!")

  while True:
    user_input = input("Arcane Scribe> ").strip() # Prompt for user input.

    if not user_input: # Skip if the input is empty.
        continue

    input_lower = user_input.lower() # Convert input to lowercase for command matching.

    try: # Wrap main command dispatch in try-except to catch errors gracefully.
      if input_lower == "vanish":
        print("Farewell, seeker of numerical truths! May your path be free of rogue decimals.")
        break # Exit the loop, terminating the program.

      elif input_lower == "help":
        # Display the themed help message.
        print("""
The Oracle's Guide to the Calculator of Whimsy:
------------------------------------------------
Enter expressions like '3 * (4 + 2) - 7 / 2 ^ 3' to unveil their secrets.
Available Spells (Commands):
  m+ <expression>   : Infuse the result of <expression> into the Memory Crystal.
  m- <expression>   : Withdraw the essence of <expression> from the Memory Crystal.
  mr                : Reveal the Memory Crystal's current enchantment (value).
  mc                : Cleanse the Memory Crystal with a mystical breeze.
  scrolls           : Unfurl the Chronicles of Calculations Past (your history).
  help              : Display this Oracle's Guide.
  vanish            : Depart from this realm of calculation.
May your calculations be ever precise!
""")
      elif input_lower == "scrolls":
        # Display the calculation history.
        print("\n=== The Grand Scroll of Calculations Past ===")
        if not calculation_history:
          print("The scroll is blank... for now. Go forth and calculate!")
        else:
          for i, entry in enumerate(calculation_history, 0):
            print(f"Record {i+1}: {entry}") # Numbered history entries.
        print("==========================================")

      elif input_lower == "mr": # Memory Recall
        current_memory_value = memory_recall()
        print(f"The Memory Crystal whispers its value: {current_memory_value}")

      elif input_lower == "mc": # Memory Clear
        memory_clear()
        calculation_history.append("Memory Crystal cleansed by a mystical breeze.")
        print("A mystical breeze has cleansed the Memory Crystal. It now holds 0.0.")

      elif input_lower.startswith("m+ "): # Add to Memory
        sub_expression = user_input[3:].strip() # Extract the expression part.
        if not sub_expression:
          print("To enchant the Memory Crystal with m+, you must provide an expression after the command!")
        else:
          try:
            value_to_add = evaluate_expression(sub_expression)
            memory_add(value_to_add)
            history_entry = f"m+ {sub_expression} (yielded: {value_to_add}) infused into Memory Crystal. Current enchantment: {calculator_memory}"
            calculation_history.append(history_entry)
            print(f"The Memory Crystal now gleams with {calculator_memory}, after adding {value_to_add} (from your query: {sub_expression}).")
          except ValueError as e: # Catch errors from evaluating the sub-expression.
            error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
            print(f"{error_prefix} The m+ spell fizzled! Problem with '{sub_expression}': {e}")

      elif input_lower.startswith("m- "): # Subtract from Memory
        sub_expression = user_input[3:].strip() # Extract the expression part.
        if not sub_expression:
          print("To drain the Memory Crystal with m-, you must provide an expression after the command!")
        else:
          try:
            value_to_subtract = evaluate_expression(sub_expression)
            memory_subtract(value_to_subtract)
            history_entry = f"m- {sub_expression} (yielded: {value_to_subtract}) drained from Memory Crystal. Current enchantment: {calculator_memory}"
            calculation_history.append(history_entry)
            print(f"The Memory Crystal's power is now {calculator_memory}, after subtracting {value_to_subtract} (from your query: {sub_expression}).")
          except ValueError as e: # Catch errors from evaluating the sub-expression.
            error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
            print(f"{error_prefix} The m- spell faltered! Problem with '{sub_expression}': {e}")

      else:
        # Default action: evaluate the entire input as a mathematical expression.
        result = evaluate_expression(user_input)
        calculation_history.append(f"{user_input} = {result} (as foretold by the Oracle)")
        print(f"The Oracle divines: {user_input} = {result}")

    except ValueError as e:
      # Catch ValueErrors from evaluate_expression or other themed errors raised in CLI logic.
      error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
      # Ensure the original error message (e) is included for clarity.
      print(f"{error_prefix} ({e})")
    except IndexError:
      # This might occur if string splitting for commands like m+ fails unexpectedly.
      error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
      print(f"{error_prefix} Your command was structured like a broken wand!")
    except Exception as e:
      # Catch-all for any other unexpected issues to prevent crashing.
      error_prefix = random.choice(FANTASY_ERROR_PREFIXES)
      print(f"{error_prefix} An unforeseen mystical disturbance occurred: {e}")
