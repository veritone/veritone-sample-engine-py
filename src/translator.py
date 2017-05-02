MORSE_ALPHABET = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "/",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}

INVERSE_MORSE_ALPHABET = dict((v, k) for (k, v) in MORSE_ALPHABET.items())


def decode_morse(code, position_in_string=0):

    if position_in_string < len(code):
        morse_letter = ""
        for key, char in enumerate(code[position_in_string:]):
            if char == " ":
                position_in_string = key + position_in_string + 1
                letter = INVERSE_MORSE_ALPHABET[morse_letter]
                return letter + decode_morse(code, position_in_string)
            else:
                morse_letter += char
    else:
        return ""


def encode_morse(message):

    encoded_message = ""
    for char in message:
        encoded_message += MORSE_ALPHABET[char.upper()] + " "

    return encoded_message
