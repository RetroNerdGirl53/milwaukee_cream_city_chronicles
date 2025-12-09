import sys
import time
import os

class Colors:
    """
    ANSI Color codes for a Colorful and Feminine palette.
    """
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Standard Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright/Bold Colors (The "Pop" Palette)
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # The "Feminine" Aliases
    PINK = BRIGHT_MAGENTA
    HOT_PINK = "\033[1;95m" # Bold Bright Magenta
    TEAL = CYAN
    LIGHT_BLUE = BRIGHT_CYAN
    MINT = BRIGHT_GREEN
    GOLD = YELLOW
    SPARKLE = BRIGHT_WHITE
    DANGER = RED
    LAVENDER = MAGENTA

    @staticmethod
    def style(text, color=RESET, styles=[]):
        """Applies color and styles to text."""
        style_codes = "".join(styles)
        return f"{color}{style_codes}{text}{Colors.RESET}"

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_print(text, speed=0.03, color=Colors.RESET, end="\n"):
    """
    Prints text one character at a time.
    """
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(Colors.RESET + end)

def print_centered(text, width=70, color=Colors.RESET):
    """Prints text centered within a given width."""
    lines = text.split('\n')
    for line in lines:
        print(f"{color}{line.center(width)}{Colors.RESET}")

def print_banner(text, color=Colors.PINK, border_char="~*~", width=70):
    """Prints a decorative banner."""
    border = border_char * (width // len(border_char))
    print(f"{color}{border}")
    print(f"{text.center(len(border))}")
    print(f"{border}{Colors.RESET}")

def print_separator(char="-", width=70, color=Colors.TEAL):
    """Prints a colorful separator line."""
    print(f"{color}{char * width}{Colors.RESET}")
