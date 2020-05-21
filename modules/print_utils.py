from sys import exit


# Pretty print a highlighted message
def print_highlight(arg):

    print("\u001b[1;32m" + arg + "\u001b[0m")


# Pretty print an error message and terminate excution
def print_error(arg):

    exit("\u001b[1;31mError: " + arg + "\u001b[0m")
