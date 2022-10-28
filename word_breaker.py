from Token import Token
from constants import punctuators
from helper_functions import check_end_of_string, generate_token, numbers_only


def break_into_words_and_generate_tokens(string: str) -> list[Token]:
    tokens: list[Token] = []
    str_len = len(string)
    line_number = 1
    char_index = 0
    word = ""
    is_string = is_single_line_comment = is_multi_line_comment = False

    while char_index < str_len:
        temp = string[char_index]
        char_index += 1
        if(is_single_line_comment and temp != "\n"):
            continue
        if(temp == "?" and is_multi_line_comment and string[char_index] == "#"):
            is_multi_line_comment = False
            char_index += 1
            continue
        if(is_multi_line_comment):
            if(temp == "\n"):
                line_number += 1
            continue
        # ! Quotation Mark
        if(temp == "\""):
            # ? either start of string || within string || end of string
            # ? 1. if start of string, generate token for content in word if any
            if(word != '' and not is_string):
                tokens.append(generate_token(word, line_number))
                word = ""
            # ? add quotations to word and set is_string to True
            word += temp
            is_string = True
            # ? checking if end of string, generate token if it is and set is_string to False and empty temp and word
            if(check_end_of_string(word)):
                tokens.append(generate_token(word, line_number))
                is_string = False
                word = ""
        # ! Single Line Comments0
        elif(temp == "#"):
            # ? could be part of string
            if(is_string):
                word += temp
                continue
            # ? if not then generate token for content in word and then proceed
            if(word != ""):
                tokens.append(generate_token(word, line_number))
                word = ""
            # ? check for multiline comment
            if(string[char_index] == "?"):
                is_multi_line_comment = True
            else:
                is_single_line_comment = True
        # ! Space or tab character
        elif(temp == ' ' or temp == '\t'):
            # ? could be part of string, if it is add to word and go for next iteration
            if(is_string):
                word += temp
                continue
            # ? if not generate token for content in word if any and also for temp and empty temp and word
            if(word != ''):
                tokens.append(generate_token(word, line_number))
                word = ""
        # ! new line character
        elif(temp == "\n"):
            # ? as multiline string is not supported, generate token for content in word if any and also for temp and empty temp and word
            if(word != ''):
                tokens.append(generate_token(word, line_number))
                word = ""
                is_string = False
            is_single_line_comment = False
            line_number += 1
        # ! punctuators
        elif(temp in punctuators):
            # ? could be part of string, if it is add to word and go for next iteration
            if(is_string):
                word += temp
                continue
            # ? if not part of string then decimal can be in numbers
            if(temp == "."):
                # ? check if numbers and decimals only after adding decimal
                if(numbers_only(word) and numbers_only(string[char_index])):
                    word += temp
                else:
                    if(word != ""):
                        tokens.append(generate_token(word, line_number))
                        word = ""
                    if(numbers_only(string[char_index])):
                        word += temp
                    else:
                        tokens.append(generate_token(temp, line_number))
            # ? if not decimal then generate tokens
            else:
                if(word != ""):
                    tokens.append(generate_token(word, line_number))
                    word = ""
                tokens.append(generate_token(temp, line_number))
        # ! operators
        elif(temp in ["+", "-", "*", "/", "%", "=", "<", ">", "!", "&", "|"]):
            # ? could be part of string, if it is add to word and go for next iteration
            if(is_string):
                word += temp
                continue
            # ? if not part of string first generate token for anything in word
            if(word != ''):
                tokens.append(generate_token(word, line_number))
                word = ""
            # ? check for operators that could be compund with equals
            if(temp in ["+", "-", "*", "/", "%", "=", "<", ">", "!"]):
                if(string[char_index] == "="):
                    tokens.append(generate_token(temp + "=", line_number))
                    char_index += 1
                elif(temp == "+" and string[char_index] == "+"):
                    tokens.append(generate_token(temp + "+", line_number))
                    char_index += 1
                elif(temp == "-" and string[char_index] == "-"):
                    tokens.append(generate_token(temp + "-", line_number))
                    char_index += 1
                else:
                    tokens.append(generate_token(temp, line_number))
            elif(temp == "&" and string[char_index] == "&"):
                tokens.append(generate_token(temp + "&", line_number))
                char_index += 1
            elif(temp == "|" and string[char_index] == "|"):
                tokens.append(generate_token(temp + "|", line_number))
                char_index += 1
            else:
                tokens.append(generate_token(temp, line_number))
        # ! semi colon
        elif(temp == ";"):
            # ? could be part of string, if it is add to word and go for next iteration
            if(is_string):
                word += temp
                continue
            # ? if not part of string
            if(word != ''):
                tokens.append(generate_token(word, line_number))
                word = ""
            tokens.append(generate_token(temp, line_number))
            # ? increment line number
            if(char_index == str_len):
                tokens.append(generate_token(word, line_number))
            elif(string[char_index] == "\n"):
                char_index += 1
                line_number += 1
        else:
            word += temp
            if(char_index == str_len):
                tokens.append(generate_token(word, line_number))
    return tokens
