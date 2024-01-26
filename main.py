from fpdf import FPDF
import random

class CrosswordGenerator:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = []
        self.words_given = set()

    def add_word(self, word, is_given=False):
        word = word.upper()
        for _ in range(100):  # Try 100 times to place the word
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            direction = random.choice(['horizontal', 'vertical'])

            if direction == 'horizontal' and self.can_place_word_horizontal(word, row, col):
                self.place_word_horizontal(word, row, col)
                if is_given:
                    self.words_given.add(word)  # Add word to words_given set
                return True
            elif direction == 'vertical' and self.can_place_word_vertical(word, row, col):
                self.place_word_vertical(word, row, col)
                if is_given:
                    self.words_given.add(word)  # Add word to words_given set
                return True

        return False

    def can_place_word_horizontal(self, word, row, col):
        if col + len(word) > self.size:
            return False
        for i in range(len(word)):
            if not (self.grid[row][col + i] == ' ' or self.grid[row][col + i] == word[i]):
                return False
        return True

    def can_place_word_vertical(self, word, row, col):
        if row + len(word) > self.size:
            return False
        for i in range(len(word)):
            if not (self.grid[row + i][col] == ' ' or self.grid[row + i][col] == word[i]):
                return False
        return True

    def place_word_horizontal(self, word, row, col):
        for i in range(len(word)):
            self.grid[row][col + i] = word[i]
        self.words.append((word, row, col, 'horizontal'))

    def place_word_vertical(self, word, row, col):
        for i in range(len(word)):
            self.grid[row + i][col] = word[i]
        self.words.append((word, row, col, 'vertical'))

    def fill_empty_spaces(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def create_pdf(self, filename, text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=13)

        # Get the width of the text
        text_width = pdf.get_string_width(text)

        # Calculate the x-coordinate to center the text
        x_coordinate = (pdf.w - text_width) / 2

        # Set the x-coordinate and add the centered text to the PDF
        pdf.set_x(x_coordinate)
        pdf.cell(0, 10, text, ln=True)

        # Add crossword grid and key (these lines now also use centered text)
        grid_width = len(self.grid[0]) * 6
        x_coordinate_grid = (pdf.w - grid_width) / 2

        for row in self.grid:
            pdf.set_x(x_coordinate_grid)
            for cell in row:
                pdf.cell(6, 6, cell, border=1)
            pdf.ln(6)

        pdf.ln(6)  # Add some space between the grid and the words

        pdf.cell(0, 6, txt="Key:", ln=True, align='C')
        for word, _, _, _ in self.words:
            pdf.cell(0, 6, txt=word, ln=True, align='C')

        pdf.output(filename)

# Prompt user for words
def prompt_for_words():
    words = []
    print("Enter words for the crossword puzzle (type 'done' when finished):")
    while True:
        word = input("> ").strip()
        if word.lower() == 'done':
            break
        if word:
            words.append(word.upper())
    return words

# Example usage
generator = CrosswordGenerator(size=20)
words_to_add = prompt_for_words()
for word in words_to_add:
    if not generator.add_word(word):
        print(f"Warning: Couldn't place the word '{word}' in the puzzle.")
generator.fill_empty_spaces()
generator.create_pdf("crossword.pdf", "Crossword Puzzle:")
