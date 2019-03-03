def has_alphanum_chars(string):
    has_letters = any(char.isalpha() for char in string)
    has_numbers = any(char.isdigit() for char in string)

    return has_letters and has_numbers
