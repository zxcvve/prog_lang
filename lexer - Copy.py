import re

class Lexer:
    def __init__(self):
        self.WHITESPACE = {' ', '\t', '\n'}

        self.TOKEN_REGEX = [
            (r':=', 'ASSIGN'),
            (r'writeln', 'WRITELN'),
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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.error_occurred = False

    def consume_token(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def match(self, expected_token_type):
        if self.current_token and self.current_token[0] == expected_token_type:
            self.consume_token()
        else:
            # raise SyntaxError(f"Expected {expected_token_type}, but found {self.current_token[0]}")
            if(self.current_token):
                self.error_occurred = True
                print(F"Syntax Error: Expected {expected_token_type}, but found {self.current_token[0]}")

    def program(self):
        self.match('PROGRAM')
        self.match('ID')
        self.match('SEMICOLON')
        self.declarations()
        self.match('BEGIN')
        self.statement_list()
        self.match('END')

    def declarations(self):
        if self.current_token and self.current_token[0] == 'VAR':
            self.match('VAR')
            self.variable_list()
            self.match('SEMICOLON')

    def variable_list(self):
        while self.current_token and self.current_token[0] == ('ID' or 'COMMA'):
            self.match('ID')
            if self.current_token and self.current_token[0] == 'COMMA':
                self.match('COMMA')

    def statement_list(self):
        self.statement()
        while self.current_token and self.current_token[0] == 'SEMICOLON':
            self.match('SEMICOLON')
            self.statement()

    def statement(self):
        if self.current_token and self.current_token[0] == 'ID':
            self.match('ID')
            self.match('ASSIGN')
            self.expression()
        elif self.current_token and self.current_token[0] == 'IF':
            self.match('IF')
            self.expression()
            self.match('THEN')
            self.statement_list()
            if self.current_token and self.current_token[0] == 'ELSE':
                self.match('ELSE')
                self.statement_list()
        elif self.current_token and self.current_token[0] == 'WHILE':
            self.match('WHILE')
            self.expression()
            self.match('DO')
            self.statement_list()
        elif self.current_token and self.current_token[0] == 'WRITELN':
            self.match('WRITELN')
            self.match('LPAREN')
            self.expression()
            self.match('RPAREN')

    def expression(self):
        self.simple_expression()
        if self.current_token and self.current_token[0] in ['EQUALS', 'GTHAN', 'LTHAN']:
            self.match(self.current_token[0])
            self.simple_expression()

    def simple_expression(self):
        self.term()
        while self.current_token and self.current_token[0] in ['PLUS', 'MINUS']:
            self.match(self.current_token[0])
            self.term()

    def term(self):
        self.factor()
        while self.current_token and self.current_token[0] in ['TIMES', 'DIVIDE']:
            self.match(self.current_token[0])
            self.factor()

    def factor(self):
        if self.current_token and self.current_token[0] == 'ID':
            self.match('ID')
        elif self.current_token and self.current_token[0] == 'NUMBER':
            self.match('NUMBER')
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self.match('LPAREN')
            self.expression()
            self.match('RPAREN')
        else:
            self.error_occurred = True
            print(f"Invalid factor: {self.current_token[0]}")   

if __name__ == "__main__":
    input_text = """
    program HelloWorld;
    var
        x,y;
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

    parser = Parser(tokens)
    parser.program()
    if parser.error_occurred == False:
        print("Синтаксических ошибок не обнаружено")
