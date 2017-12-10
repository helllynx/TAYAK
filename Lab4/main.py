import sys
sys.path.insert(0, "../..")

import ply.lex as lex
import ply.yacc as yacc
import os

import math

line_number = 0

reserved_names = ['int', 'bool', 'void', 'print', 'if', 'while', 'for', 'True', 'False']

class Parser(object):
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        # while 1:
        try:
            with open('main.cpp', 'r') as content_file:
                for line in content_file.readlines():
                    global line_number
                    line_number += 1
                    if(line!='\n'):
                        yacc.parse(line)
            # with open('main.cpp', 'r') as content_file:
            #     yacc.parse(content_file.read())
        except EOFError:
            print("Input empty!")


def perror(text):
    global line_number
    print("ERROR " + str(line_number) +  ": "+ text)


class Eval(Parser):

    tokens = (
        'NUMBER','TYPE','IDENTIFIER', 'PROGRAM',
        'ASSIGN', 'RETURN','PRINT', 'BOOL',
        'IF', 'BOOL_EXPRESSION','FOR', 'GT', 'LT', 'EQUALS', 'NOT_EQUAL',
        'PLUS', 'MINUS', 'UMINUS', 'EXP', 'TIMES', 'DIVIDE',
        'LPAREN', 'RPAREN', 'COMMA', 'COLON', 'LBRACE', 'RBRACE'
    )

    # Tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EXP = r'\*\*'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_GT = r'>'
    t_LT = r'<'
    t_EQUALS = r'=='
    t_NOT_EQUAL = r'!='
    # t_PRINT = r'print\(\b(?!int|void|bool)([a-zA-Z_][a-zA-Z0-9_]*)\)'
    t_PRINT = r'print'
    t_IF = r'\bif\b'
    t_FOR = r'\bfor\b'


    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_BOOL = r'True|False'
    t_IDENTIFIER = r'\b(?!' + '|'.join(reserved_names) + r')[a-zA-Z_][a-zA-Z0-9_]*'

    t_COMMA = r','
    t_COLON = r':'
    t_RETURN = r'return'
    t_TYPE = r'int|bool|void'


    def exist(self, p):
        if (self.names.__contains__(p)):
            return True
        else:
            perror('variable ' + str(p) + ' not exist')
            return False

    def t_NUMBER(self, t):
        r'[0-9]*[.]?[0-9]+'
        try:
            t.value = float(t.value)
        except ValueError:
            perror("Integer value too large %s" % t.value)
            t.value = 0
        return t


    # Completely ignored characters
    t_ignore = ' \t\x0c'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        perror("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)



    # Parsing rules
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'ASSIGN'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),
    )

    def p_print(self, p):
        'expression : PRINT LPAREN expression RPAREN'
        print(p[3])

    def p_if(self ,p):
        'expression : IF LPAREN expression RPAREN'
        pass

    def p_for(self,p):
        'expression : FOR LPAREN TYPE IDENTIFIER ASSIGN NUMBER COMMA expression RPAREN'

    def p_statement_assign(self, p):
        """expression : IDENTIFIER ASSIGN IDENTIFIER
                        |   IDENTIFIER ASSIGN BOOL
                        |   IDENTIFIER ASSIGN NUMBER
                        |   IDENTIFIER ASSIGN expression
        """
        if(self.exist(p[1]) and self.exist(p[3])):
            self.names[p[1]] = self.names[p[3]]
            print('assign var ' + p[1] + " " + str(p[3])+" = " + str(self.names[p[3]]))
        elif(self.exist(p[1])):
            self.names[p[1]] = p[3]
            print('assign ' + p[1] + " " + str(p[3]))


    # def p_statement_expr(self, p):
    #     'statement : expression'
    #     print(p[1])

    def p_expression_math_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
        """
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]

    def p_expression_bool(self, p):
        """
        expression : expression LT expression
                  | expression GT expression
                  | expression EQUALS expression
                  | expression NOT_EQUAL expression
        """
        if p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '!=':
            p[0] = p[1] != p[3]

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_NUMBER(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : IDENTIFIER'
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            perror("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_expression_declaration(self, p):
        """expression : TYPE IDENTIFIER ASSIGN NUMBER
                    | TYPE IDENTIFIER ASSIGN expression
                    | TYPE IDENTIFIER ASSIGN BOOL
                    | TYPE IDENTIFIER
        """
        if(len(p)==5):
            if p[1]=='int':
                try:
                    int(p[4])
                    self.names[p[2]] = p[4] or 0
                except:
                    perror("Assign value not INT!")
            elif p[1]=='void':
                if(p[4]!=''):
                    perror('You can not assign a value to a type void')
            elif p[1]=='bool':
                try:
                    bool(p[4])
                    self.names[p[2]] = bool(p[4]) or False
                except:
                    perror("Assign value not bool!")
        else:
            self.names[p[2]] = None

    def p_error(self, p):
        if p:
            perror("Syntax error at '%s'" % p.value)
        else:
            perror("Syntax error at EOF")




if __name__ == '__main__':
    calc = Eval()
    calc.run()
