from fpdf import FPDF
import random

class CrosswordGenerator:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = []

    def add_word(self, word):
        word = word.upper()
        for _ in range(100):  # Try 100 times to place the word
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - len(word))
            if self.can_place_word(word, row, col):
                self.place_word(word, row, col)
                return True
        return False

    def can_place_word(self, word, row, col):
        for i in range(len(word)):
            if self.grid[row][col + i] not in (' ', word[i]):
                return False
        return True

    def place_word(self, word, row, col):
        for i in range(len(word)):
            self.grid[row][col + i] = word[i]
        self.words.append(word)

    def fill_empty_spaces(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def create_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=13)

        # Add crossword grid to PDF
        pdf.cell(200, 6, txt="Crossword Puzzle:", ln=True)
        for row in self.grid:
            line = ' '.join(row)
            pdf.cell(200, 6, txt=line, ln=True)

        # Add key to PDF
        pdf.cell(200, 6, txt="Key:", ln=True)
        for word in self.words:
            pdf.cell(200, 6, txt=word, ln=True)

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
generator = CrosswordGenerator(size=10)
words_to_add = prompt_for_words()
for word in words_to_add:
    if not generator.add_word(word):
        print(f"Warning: Couldn't place the word '{word}' in the puzzle.")
generator.fill_empty_spaces()
generator.create_pdf("crossword.pdf")
