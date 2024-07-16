# This script will list the examples in the examples folder and run the selected example using mpremote.
# The user can select the example using the arrow keys.
# To run the script, use the following command:
# python run_examples.py

import os

def get_examples():
    # Reads the examples from the examples folder
    examples = []
    for filename in os.listdir('examples'):
        if filename.endswith('.py'):
            examples.append(filename)
    return examples

def run_example(example):
    # Run the example using mpremote: mpremote mount src run ./examples/{example}
    os.system(f'mpremote mount src run ./examples/{example}')

if __name__ == '__main__':
    examples = get_examples()

    # Ask the user which example to run using the arrow keys
    import curses
    from curses import wrapper
    from curses.textpad import Textbox, rectangle

    def main(stdscr):
        global examples
        curses.curs_set(0)
        main_text_start_row = 2
        selected_row = 0

        while True:
            try:
                # Refresh curses.LINES to get the latest terminal size
                curses.update_lines_cols()

                # Check if the terminal size is large enough to display the examples
                if curses.LINES < len(examples) + main_text_start_row:
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Increase the terminal size to display the examples.")
                    stdscr.refresh()
                    continue

                stdscr.clear()  # Clear the screen before repainting
                stdscr.addstr(0, 0, "Select an example to run:")
                
                for i, example in enumerate(examples):
                    x = 0 if i == selected_row else 2
                    y = main_text_start_row + i

                    if i == selected_row:
                        stdscr.addstr(y, x, f"> {example}", curses.A_BOLD)
                        stdscr.addstr(y, x + len(example) + 2, ' ')
                    else:
                        stdscr.addstr(y, x, example)
                
                stdscr.refresh()            
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    selected_row = max(0, selected_row - 1)
                elif key == curses.KEY_DOWN:
                    selected_row = min(len(examples) - 1, selected_row + 1)
                elif key == ord('\n'):                
                    # Ensure the screen is cleared before running the example
                    stdscr.clear()                
                    stdscr.refresh()
                    run_example(examples[selected_row])
                    # break # Uncomment this line to exit the loop after running one example
            except KeyboardInterrupt:
                break

    wrapper(main)