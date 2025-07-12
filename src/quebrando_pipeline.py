import os, sys  # F401 (unused imports), E401 (multiple imports on one line)

def soma(a,b):  # E231 (missing whitespace after comma), E302 (expected 2 blank lines before def)
  return a+b     # E111 (indentation), E225 (missing whitespace around operator)

def exemplo():
    print('Olá mundo')  # S101 (use of print is discouraged)

try:
    resultado = soma(1, 2)
except Exception as e:  # BLE001 (blind except), EM102 (f-string in exception)
    raise RuntimeError(f"Erro: {e}")