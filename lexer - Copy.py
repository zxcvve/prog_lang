import re
import re

class Lexer:
    def __init__(self):
        self.WHITESPACE = {' ', '\t', '\n'}

        self.TOKEN_REGEX = [
            (r':=', 'IS'),
            (r'\bprogram\b', 'PROGRAM'),
            (r'\bvar\b', 'VAR'),
            (r'\bbegin\b', 'BEGIN'),
            (r'\bend\b', 'END'),
            (r'\bif\b', 'IF'),
            (r'\bthen\b', 'THEN'),
            (r'\belse\b', 'ELSE'),
            (r'\bwhile\b', 'WHILE'),
            (r'\bdo\b', 'DO'),
            (r'\bdiv\b', 'DIV'),
            (r'\bmod\b', 'MOD'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),
            (r'\d+', 'NUMBER'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'TIMES'),
            (r'/', 'DIVIDE'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'=', 'EQUALS'),
            (r';', 'SEMICOLON'),
            (r',', 'COMMA'),
            (r':', 'COLON'),
            (r'>', 'GTHAN'),
            (r'<', 'LTHAN'),
        ]

    def error_handler(self, line, position, error_type):
        print(f"Error at line {line}, position {position}: {error_type}")

    def lex(self, input_text):
        tokens = []
        line = 1
        position = 0

        while position < len(input_text):
            match = None

            for pattern, token_type in self.TOKEN_REGEX:
                regex = re.compile(pattern)
                match = regex.match(input_text, position)
                if match:
                    token = match.group(0)
                    tokens.append((token_type, token, line))
                    position = match.end()
                    break

            if not match:
                char = input_text[position]
                if char in self.WHITESPACE:
                    if char == '\n':
                        line += 1
                    position += 1
                else:
                    self.error_handler(line, position, f"Invalid character: {char}")
                    position += 1

        return tokens

if __name__ == "__main__":
    input_text = """
    program HelloWorld;
    var
      x, y: integer;
    begin
      x := 10;
      y := 20;
      if x > y then
        writeln(x)
      else
        writeln(y)
    end
    """

    lexer = Lexer()
    
    tokens = lexer.lex(input_text)
    for token_type, token, line in tokens:
        print(f"Token: {token_type}, Lexeme: {token}, Line: {line}")


