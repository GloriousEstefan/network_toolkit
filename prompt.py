from re import finditer
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.lexers import Lexer
from main import ScriptLoop, open_file
from getpass import getpass
from pyfiglet import figlet_format


def help():
    for key, value in command_defs.items():
        print(f"\033[32m{key}\033[0m: {value}")


class CustomLexer(Lexer):
    def lex_document(self, document):
        # List of words you want to search for
        search_words = ["^" + word + "\ " for word in list(command_funcs.keys())]

        def get_line(lineno):
            line = document.lines[lineno]
            word_indices = []

            for search_word in search_words:
                word_indices.extend([(m.start(), m.end(), search_word) for m in finditer(search_word, line)])

            # Sort the word_indices by their starting positions
            word_indices.sort(key=lambda x: x[0])

            styled_line = []
            i = 0

            for start, end, search_word in word_indices:
                # Add the text before the search_word with no color
                styled_line.append(("", line[i:start]))

                # Add the search_word with a color
                styled_line.append(("ansigreen", line[start:end]))

                # Update the index
                i = end

            # Add the remaining text after the last search_word with no color
            styled_line.append(("", line[i:]))

            return styled_line

        return get_line


multi_send = ScriptLoop(username="", password="")


command_funcs = {
    "help": help,
    "list": open_file,
    "run": multi_send.run_script,
}


command_defs = {
    "help": "List all available commands",
    "list": "Open IP list text file for ",
    "run": "Send command via SSH to all devices in list",
}


def main():
    session = PromptSession(
        lexer=CustomLexer()
    )
    
    while True:
        text = session.prompt(">>> ")

        if not text.strip():
            continue
            
        args = text.split()
        command = args[0]

        if command == "exit":
            break

        if command not in command_funcs:
            print(f"{command} is not a known command")
        
        if command in command_funcs and len(args) == 1:
            try:
                command_funcs[args[0]]()

            except TypeError:
                print("Too many arguements entered")
                continue

        if command in command_funcs and len(args) > 1:
            try:
                command_funcs[command](args[1:])
                
            except TypeError:
                    print("Missing an arguement")
                    continue
            

if __name__ == "__main__":
    print(figlet_format("Network Toolkit", font="larry3d"))
    main()
