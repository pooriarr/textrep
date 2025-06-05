import tkinter as tk
from tkinter import messagebox # For themed error dialogs later
import calculator # To access evaluate_expression, memory functions, history, etc.
import random # For themed error prefixes from calculator module

# --- Main Application Class ---
class CalculatorApp:
    def __init__(self, root_window):
        self.root = root_window
        # Updated Window Title
        self.root.title("The Calculator of Whimsy")
        self.root.geometry("400x700")

        self.expression_str = ""
        self.current_input = ""
        self.just_evaluated = False

        # --- Consolidated & Refined Theming ---
        self.bg_color = "#f0e6d2"                       # Parchment-like background
        self.display_bg_color = "#ffffff"               # Clear crystal/paper
        self.text_color = "#3b3a30"                     # Dark ink (for most text)

        self.digit_button_color = "#e0d6c7"             # Lighter parchment/bone for digits
        self.operator_button_color = "#c8b8a8"         # Slightly darker stone for operators, ⌫, Scrolls
        self.memory_button_color = "#708090"            # Slate gray for memory (MC, MR, M+, M-)
        self.ac_button_color = "#c0392b"                # Reddish for AC (was e74c3c)
        self.ce_button_color = "#d35400"                # Orangish for CE (was e67e22)
        self.equals_button_bg_color = "#8c785c"         # Antique brass/dark wood for Equals

        self.control_text_color = "white"               # For buttons with dark backgrounds (AC, CE, Memory, Equals)
        self.scrolls_button_color = self.operator_button_color # Scrolls uses operator styling

        # --- Font Definitions ---
        self.default_font_family = "Georgia"
        self.display_font_family = "Georgia" # Changed to Georgia for thematic consistency
        # Note: Specific "fantasy" fonts like Papyrus are often not universally available.
        # Georgia provides a readable, somewhat old-style, serif look.

        self.display_font = (self.display_font_family, 28)
        self.button_font = (self.default_font_family, 15)
        self.button_font_bold = (self.default_font_family, 15, 'bold')
        self.scrolls_font = (self.default_font_family, 14, 'bold') # Font for Scrolls button, slightly smaller if needed
        self.mem_indicator_font = (self.default_font_family, 10, 'bold')
        self.history_text_font = (self.default_font_family, 12)
        self.history_button_font = (self.default_font_family, 12, 'bold')


        self.root.configure(bg=self.bg_color)

        self.display_frame = tk.Frame(self.root, bg=self.bg_color)
        self.display_frame.pack(pady=(10,5), padx=10, fill="x")

        self.display_frame.columnconfigure(0, weight=0)
        self.display_frame.columnconfigure(1, weight=1)

        self.memory_indicator_var = tk.StringVar(value="")
        self.memory_indicator_label = tk.Label(self.display_frame, textvariable=self.memory_indicator_var,
                                              font=self.mem_indicator_font, bg=self.display_bg_color,
                                              fg=self.text_color, width=3, anchor='w')
        self.memory_indicator_label.grid(row=0, column=0, sticky='nsew', padx=(2,0))

        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display_entry = tk.Entry(self.display_frame, textvariable=self.display_var,
                                      font=self.display_font, bg=self.display_bg_color,
                                      fg=self.text_color, borderwidth=3, relief=tk.SUNKEN,
                                      justify='right', state='readonly')
        self.display_entry.grid(row=0, column=1, sticky='nsew', ipady=10)

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=(5,10), padx=10, expand=True, fill="both")

        self.button_layout = [
            ['MC', 'MR', 'M-', 'M+'],
            ['AC', 'CE', '⌫', 'Scrolls'],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '^', '+']
        ]

        for r, row_content in enumerate(self.button_layout):
            for c, text in enumerate(row_content):
                btn_config = {
                    'font': self.button_font,
                    'relief': tk.RAISED, 'borderwidth': 2,
                    'bg': self.digit_button_color, 'fg': self.text_color
                }
                cmd = None

                if text == 'AC':
                    btn_config.update({'bg': self.ac_button_color, 'fg': self.control_text_color, 'font': self.button_font_bold})
                    cmd = self._on_ac_click
                elif text == 'CE':
                    btn_config.update({'bg': self.ce_button_color, 'fg': self.control_text_color, 'font': self.button_font_bold})
                    cmd = self._on_ce_click
                elif text == '⌫':
                    btn_config.update({'bg': self.operator_button_color})
                    cmd = self._on_backspace_click
                elif text == 'Scrolls':
                    btn_config.update({'bg': self.scrolls_button_color, 'font': self.scrolls_font, 'fg': self.text_color}) # Ensure text_color if not control_text_color
                    cmd = self._on_scrolls_click
                elif text == 'MC':
                    btn_config.update({'bg': self.memory_button_color, 'fg': self.control_text_color, 'font': self.button_font}) # Memory buttons use normal weight font
                    cmd = self._on_mc_click
                elif text == 'MR':
                    btn_config.update({'bg': self.memory_button_color, 'fg': self.control_text_color, 'font': self.button_font})
                    cmd = self._on_mr_click
                elif text == 'M-':
                    btn_config.update({'bg': self.memory_button_color, 'fg': self.control_text_color, 'font': self.button_font})
                    cmd = self._on_m_subtract_click
                elif text == 'M+':
                    btn_config.update({'bg': self.memory_button_color, 'fg': self.control_text_color, 'font': self.button_font})
                    cmd = self._on_m_add_click
                elif text in ['/', '*', '-', '+', '^']:
                    btn_config.update({'bg': self.operator_button_color})
                    cmd = lambda t=text: self._on_button_click(t)
                else: # Digits and '.'
                    cmd = lambda t=text: self._on_button_click(t)

                button = tk.Button(self.button_frame, text=text, command=cmd, **btn_config)
                button.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        num_cols = len(self.button_layout[0]) if self.button_layout else 4
        num_rows_main_grid = len(self.button_layout)

        for i in range(num_cols):
            self.button_frame.columnconfigure(i, weight=1)
        for i in range(num_rows_main_grid):
            self.button_frame.rowconfigure(i, weight=1)

        equals_button_row = num_rows_main_grid
        self.equals_button = tk.Button(self.button_frame, text="=",
                                   font=self.button_font_bold, # Use bold button font
                                   bg=self.equals_button_bg_color,
                                   fg=self.control_text_color, # Use control_text_color for dark bg
                                   relief=tk.RAISED,
                                   borderwidth=3,
                                   command=self._on_equals_click)
        self.equals_button.grid(row=equals_button_row, column=0, columnspan=num_cols, padx=2, pady=4, sticky="nsew")
        self.button_frame.rowconfigure(equals_button_row, weight=1)

        self._update_memory_indicator()

    def _update_memory_indicator(self):
       if calculator.calculator_memory != 0: self.memory_indicator_var.set(" M ")
       else: self.memory_indicator_var.set("")

    def _on_mc_click(self):
       calculator.memory_clear(); self._update_memory_indicator(); self.just_evaluated = False

    def _on_mr_click(self):
       recalled_value = calculator.memory_recall()
       val_str = str(int(recalled_value)) if isinstance(recalled_value, float) and recalled_value.is_integer() else f"{recalled_value:.10g}"
       self.display_var.set(val_str); self.current_input = val_str; self.expression_str = ""; self.just_evaluated = False

    def _get_value_for_memory_op(self):
       val_to_operate_on_str = self.current_input if self.current_input and self.current_input != "Error" else self.display_var.get()
       if val_to_operate_on_str in ['+', '-', '*', '/', '^', '%', 'Error'] or not val_to_operate_on_str:
           error_prefix = random.choice(calculator.FANTASY_ERROR_PREFIXES)
           messagebox.showerror("Memory Crystal Error!", f"{error_prefix}\nNo valid number for memory op (Value: '{val_to_operate_on_str}').", parent=self.root)
           return None
       try: return float(val_to_operate_on_str)
       except ValueError:
           error_prefix = random.choice(calculator.FANTASY_ERROR_PREFIXES)
           messagebox.showerror("Memory Crystal Error!", f"{error_prefix}\nInvalid number ('{val_to_operate_on_str}') for memory op.", parent=self.root)
           return None

    def _on_m_add_click(self):
       value = self._get_value_for_memory_op()
       if value is not None:
           calculator.memory_add(value); self._update_memory_indicator()
           history_entry = f"M+ {value:.10g} -> Memory now {calculator.calculator_memory:.10g}"
           if not calculator.calculation_history or calculator.calculation_history[-1] != history_entry: calculator.calculation_history.append(history_entry)
           self.just_evaluated = True; self.current_input = str(value) if not (isinstance(value,float) and value.is_integer()) else str(int(value))

    def _on_m_subtract_click(self):
       value = self._get_value_for_memory_op()
       if value is not None:
           calculator.memory_subtract(value); self._update_memory_indicator()
           history_entry = f"M- {value:.10g} -> Memory now {calculator.calculator_memory:.10g}"
           if not calculator.calculation_history or calculator.calculation_history[-1] != history_entry: calculator.calculation_history.append(history_entry)
           self.just_evaluated = True; self.current_input = str(value) if not (isinstance(value,float) and value.is_integer()) else str(int(value))

    def _on_ac_click(self):
        self.expression_str = ""; self.current_input = ""; self.display_var.set("0"); self.just_evaluated = False

    def _on_ce_click(self):
        if self.just_evaluated: self._on_ac_click()
        else: self.current_input = ""; self.display_var.set("0")

    def _on_backspace_click(self):
        if self.just_evaluated: self.current_input = ""; self.expression_str = ""; self.display_var.set("0"); self.just_evaluated = False; return
        current_display_val = self.display_var.get()
        if current_display_val == "Error": self._on_ac_click(); return
        if current_display_val in ['+', '-', '*', '/', '^', '%'] and not self.current_input: pass
        elif self.current_input: self.current_input = self.current_input[:-1]; self.display_var.set(self.current_input if self.current_input else "0")

    def _on_button_click(self, char_clicked):
        if (char_clicked.isdigit() or char_clicked == '.') and self.just_evaluated:
            self.current_input = ""; self.expression_str = ""; self.just_evaluated = False
        elif char_clicked in ['+', '-', '*', '/', '^', '%'] and self.just_evaluated and self.current_input:
            self.expression_str = self.current_input; self.current_input = ""; self.just_evaluated = False
        elif char_clicked in ['+', '-', '*', '/', '^', '%']: self.just_evaluated = False
        display_text = self.display_var.get()
        if char_clicked.isdigit() or char_clicked == '.':
            if (display_text == "0" and char_clicked != '.') or display_text in ['+', '-', '*', '/', '^', '%']:
                if char_clicked == '.': self.current_input = "0."
                else: self.current_input = char_clicked
            else:
                if char_clicked == '.' and '.' in self.current_input: return
                self.current_input += char_clicked
            self.display_var.set(self.current_input)
        elif char_clicked in ['+', '-', '*', '/', '^', '%']:
            if self.current_input: self.expression_str += self.current_input; self.current_input = ""
            stripped_expr_val = self.expression_str.strip()
            if stripped_expr_val and stripped_expr_val[-1] in ['+', '-', '*', '/', '^', '%']:
                self.expression_str = stripped_expr_val[:-1].strip() + f" {char_clicked} "
            else: self.expression_str += f" {char_clicked} "
            self.display_var.set(char_clicked)

    def _on_equals_click(self):
        if self.current_input: self.expression_str += self.current_input
        if not self.expression_str.strip():
            self.display_var.set("0"); self.expression_str = ""; self.current_input = ""; self.just_evaluated = False; return
        try:
            expression_for_history = self.expression_str.strip()
            result = calculator.evaluate_expression(self.expression_str.strip())
            result_str = str(int(result)) if isinstance(result, float) and result.is_integer() else f"{result:.10g}"
            self.display_var.set(result_str)
            history_entry = f"{expression_for_history} = {result_str} (GUI Oracle)"
            if not calculator.calculation_history or calculator.calculation_history[-1] != history_entry:
                calculator.calculation_history.append(history_entry)
            self.expression_str = ""; self.current_input = result_str; self.just_evaluated = True
        except ValueError as e:
            error_prefix = random.choice(calculator.FANTASY_ERROR_PREFIXES)
            messagebox.showerror("A Gremlin's Mischief!", f"{error_prefix}\n{e}", parent=self.root) # Themed title
            self.display_var.set("Error"); self.expression_str = ""; self.current_input = ""; self.just_evaluated = False
        except Exception as e:
            error_prefix = random.choice(calculator.FANTASY_ERROR_PREFIXES)
            messagebox.showerror("Mystical Disturbance!", f"{error_prefix}\nAn unforeseen disturbance: {e}", parent=self.root) # Themed title
            self.display_var.set("Error"); self.expression_str = ""; self.current_input = ""; self.just_evaluated = False

    def _on_scrolls_click(self):
       if not calculator.calculation_history:
           themed_title = "The Oracle's Empty Scroll" # Already themed
           messagebox.showinfo(themed_title, "The scroll is blank... for now. Go forth and calculate, brave adventurer!", parent=self.root)
           return
       history_window = tk.Toplevel(self.root)
       history_window.title("Chronicles of Calculations Past")
       history_window.geometry("380x450"); history_window.configure(bg=self.bg_color); history_window.minsize(300, 200)
       text_frame = tk.Frame(history_window, bg=self.bg_color); text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
       history_text_widget = tk.Text(text_frame, wrap=tk.WORD, font=self.history_text_font,
                                     bg=self.display_bg_color, fg=self.text_color,
                                     borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
       scrollbar = tk.Scrollbar(text_frame, command=history_text_widget.yview, relief=tk.FLAT, troughcolor=self.bg_color)
       history_text_widget.configure(yscrollcommand=scrollbar.set)
       scrollbar.pack(side=tk.RIGHT, fill=tk.Y); history_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       history_title = "=== The Grand Scroll of Calculations Past ===\n\n"
       history_text_widget.insert(tk.END, history_title)
       for i, entry in enumerate(calculator.calculation_history):
           history_text_widget.insert(tk.END, f"Record {i+1}: {str(entry)}\n")
       history_text_widget.configure(state='disabled')
       close_button = tk.Button(history_window, text="Close Scroll", command=history_window.destroy,
                                font=self.history_button_font, bg=self.button_color, fg=self.text_color,
                                relief=tk.RAISED, borderwidth=2, padx=10)
       close_button.pack(pady=(0, 10))
       history_window.transient(self.root); history_window.grab_set(); self.root.wait_window(history_window)

# --- Main Execution Block ---
if __name__ == "__main__":
    calculator.calculator_memory = 0.0
    calculator.calculation_history = []
    main_window = tk.Tk()
    app = CalculatorApp(main_window)
    main_window.mainloop()
