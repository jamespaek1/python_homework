# Task 1: Hello
def hello():
    return "Hello!"


# Task 2: Greet with a Formatted String
def greet(name):
    return f"Hello, {name}!"


# Task 3: Calculator
def calc(a, b, operation="multiply"):
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        elif operation == "modulo":
            return a % b
        elif operation == "int_divide":
            return a // b
        elif operation == "power":
            return a ** b
        else:
            return None
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"


# Task 4: Data Type Conversion
def data_type_conversion(value, data_type):
    try:
        if data_type == "float":
            return float(value)
        elif data_type == "str":
            return str(value)
        elif data_type == "int":
            return int(value)
        else:
            return f"You can't convert {value} into a {data_type}."
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {data_type}."


# Task 5: Grading System, Using *args
def grade(*args):
    try:
        average = sum(args) / len(args)

        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except Exception:
        return "Invalid data was provided."


# Task 6: Use a For Loop with a Range
def repeat(string, count):
    result = ""
    for _ in range(count):
        result += string
    return result


# Task 7: Student Scores, Using **kwargs
def student_scores(option, **kwargs):
    if option == "best":
        return max(kwargs, key=kwargs.get)
    elif option == "mean":
        return sum(kwargs.values()) / len(kwargs)
    return None


# Task 8: Titleize, with String and List Operations
def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = text.split()

    if not words:
        return ""

    result = []

    for i, word in enumerate(words):
        word_lower = word.lower()

        if i == 0 or i == len(words) - 1:
            result.append(word_lower.capitalize())
        elif word_lower in little_words:
            result.append(word_lower)
        else:
            result.append(word_lower.capitalize())

    return " ".join(result)


# Task 9: Hangman, with more String Operations
def hangman(secret, guess):
    result = ""

    for char in secret:
        if char in guess:
            result += char
        else:
            result += "_"

    return result


# Task 10: Pig Latin, Another String Manipulation Exercise
def pig_latin(text):
    vowels = "aeiou"

    def convert_word(word):
        if word[0] in vowels:
            return word + "ay"

        index = 0
        while index < len(word):
            if word[index:index + 2] == "qu":
                index += 2
                break
            elif word[index] in vowels:
                break
            else:
                index += 1

        return word[index:] + word[:index] + "ay"

    words = text.split()
    converted = []

    for word in words:
        converted.append(convert_word(word))

    return " ".join(converted)