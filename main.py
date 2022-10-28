from Token import Token
from word_breaker import break_into_words_and_generate_tokens
from file_functions import read_file, write_to_file
from Token import Token

file_content = read_file('text/input.txt')

tokens = break_into_words_and_generate_tokens(file_content)

# ! Add end marker to token set
tokens.append(Token("end_marker", "$", -1))

write_to_file('text/output.txt', tokens)
