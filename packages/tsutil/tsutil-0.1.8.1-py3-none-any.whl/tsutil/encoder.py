# -*- coding: utf8 -*-
__morse_code__ = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',

    '1': ['.----', '.-'], '2': ['..---', '..-'], '3': ['...--', '...-'], '4': ['....-', '....-'], '5': ['.....', '.'],
    '6': ['-....', '-....'], '7': ['--...', '-...'], '8': ['---..', '-..'], '9': ['----.', '-.'], '0': ['-----', '-'],

    '.': '.-.-.-', ':': '---...', ',': '--..--', ';': '-.-.-.', '?': '..--..', '=': '-...-', "'": '.---.',
    '/': '-..-.', '!': '-.-.--', '-': '-....-', '_': '..--.-', '"': '.-..-.', '(': '-.--.', ')': '-.--.-',
    '$': '...-..-', '&': '.-...', '@': '.--.-.'
}


__de_morse_code__ = {}

for c in __morse_code__:
  if type(__morse_code__[c]) == list:
    for _c in __morse_code__[c]:
      __de_morse_code__[_c] = c
    continue
  __de_morse_code__[__morse_code__[c]] = c



def morse_encode(data):
  data = data.upper()
  encoded = []
  for c in data:
    if type(__morse_code__[c]) == list:
      encoded.append(__morse_code__[c][0])
    else:
      encoded.append(__morse_code__[c])
  return "/".join(encoded)


def morse_decode(data):
  codes = data.split("/")
  result = []
  for code in codes:
    if code:
      result.append(__de_morse_code__[code])
  return "".join(result)
