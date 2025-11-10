import sys
import re
from dataclasses import dataclass

PRINT_TOKENS = True

PRINT_PRODUCTIONS = True

USE_EXTERNAL_LEXER = False  

@dataclass
class Token:
    type: str    
    lexeme: str
    line: int


class SimpleLexer: 
    
    token_spec = [
        ("NUMBER",   r'\d+(\.\d+)?'),
        ("IDENT",    r'[A-Za-z_]\w*'),
        ("COMMENT",  r'//[^\n]*'),
        ("OP",       r'[\+\-\*/=]'),
        ("SEP",      r'[();]'),
        ("SKIP",     r'[ \t\r]+'),
        ("NEWLINE",  r'\n'),
        ("MISMATCH", r'.'),
    ]
    master = re.compile("|".join(f"(?P<{n}>{p})" for n,p in token_spec))

    def __init__(self, text: str):
        self.text = text
        
        self.pos = 0
        
        self.line = 1
        
        self._tokens = self._scan()
        
        self._index = 0


    def _scan(self):
        tokens = []
        for m in self.master.finditer(self.text):
            kind = m.lastgroup
            lex = m.group()
            if kind == "NUMBER":
                tokens.append(Token("NUMBER", lex, self.line))
            elif kind == "IDENT":
                tokens.append(Token("IDENT", lex, self.line))
            elif kind == "COMMENT":
                pass
            elif kind == "OP":
                tokens.append(Token("OP", lex, self.line))
            elif kind == "SEP":
                tokens.append(Token("SEP", lex, self.line))
            elif kind == "SKIP":
                pass
            elif kind == "NEWLINE":
                self.line += 1
            elif kind == "MISMATCH":
                tokens.append(Token("ERROR", lex, self.line))
        tokens.append(Token("EOF", "", self.line))
        return tokens

    def peek(self):
        return self._tokens[self._index]

    def next(self):
        tok = self._tokens[self._index]
        self._index += 1
        return tok
    
class ExternalLexerAdapter:
    
    """
    Replace the pass bodies with calls into your own lexer from Assignment 1.
    Your lexer must track line numbers and return (tyype, lexeme).
    """
    
    def __init__(self, text: str):

        self._fallback = SimpleLexer(text) 
    @property
    def line(self):
        return self._fallback.peek().line
    def peek(self):

        return self._fallback.peek()
    def next(self):
        return self._fallback.next()
    def _convert(self, ttype: str) -> str:
        return ttype

class Parser:
    def __init__(self, text: str, out_file):
        self.out = out_file
        self.lexer = (ExternalLexerAdapter(text) if USE_EXTERNAL_LEXER else SimpleLexer(text))
        self.lookahead = self.lexer.peek()

    def _emit_token(self, tok: Token):
        if PRINT_TOKENS:
            kind = {
                "IDENT": "Identifier",
                "NUMBER": "Number",
                "OP": "Operator",
                "SEP": "Separator",
                "EOF": "EOF",
                "ERROR": "Error"
            }.get(tok.type, tok.type)
            print(f"Token: {kind:<12} Lexeme: {tok.lexeme}", file=self.out)

    def _prod(self, text: str): 
        if PRINT_PRODUCTIONS: 
            print(f"     {text}", file=self.out)   

    def _error(self, expected):
        t = self.lookahead
        exp = ", ".join(sorted(expected))
        msg = (f"Syntax error at line {t.line}: got token '{t.type}' "
               f"lexeme '{t.lexeme}' — expected one of: {exp}")
        raise SyntaxError(msg)  

    def _match(self , ttype: str , lexeme: str =None):
        t = self.lookahead
        if t.type != ttype: 
            expected = ttype if lexeme is None else f"{ttype}('{lexeme}')"
            self._error({expected})
        if lexeme is not None and t.lexeme != lexeme:
            self._error({f"{ttype}('{lexeme}')"})
        self._emit_token (t)
        self.lexer.next()  
        self.lookahead = self.lexer.peek()
        return t  

    def parse(self ):
        self.Program ()
        if self.lookahead.type != "EOF" :
            self._error({"EOF"})
        return True

    def Program(self):
        self._prod("<Program> -> <Statements>")
        self.Statements()

    def Statements(self):
        if self.lookahead.type in {"IDENT","SEP","EOF","ERROR","NUMBER","OP"}:
            if self.lookahead.type == "IDENT":
                self._prod("<Statements> -> <Statement> <Statements>")
                self.Statement()
                self.Statements()
            else:
                self._prod("<Statements> -> ε")
                return
        else:
            self._prod("<Statements> -> ε")

    def Statement(self):
        self._prod("<Statement> -> <Assign> ;")
        self.Assign()
        self._match("SEP", ";")

    def Assign(self):
        self._prod("<Assign> -> <Identifier> = <Expression>")
        self._match("IDENT")
        self._match("OP", "=")
        self.Expression()

    def Expression(self):
        self._prod("<Expression> -> <Term> <Expression Prime>")
        self.Term()
        self.ExpressionPrime()

    def ExpressionPrime(self):
        self._prod("<Expression Prime> -> + <Term> <Expression Prime> | - <Term> <Expression Prime> | ε")
        while self.lookahead.type == "OP" and self.lookahead.lexeme in {"+","-"}:
            self._match("OP", self.lookahead.lexeme)  # + or -
            self.Term()

    def Term(self):
        self._prod("<Term> -> <Factor> <Term Prime>")
        self.Factor()
        self.TermPrime()

    def TermPrime(self):
        self._prod("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | ε")
        while self.lookahead.type == "OP" and self.lookahead.lexeme in {"*","/"}:
            self._match("OP", self.lookahead.lexeme)  # * or /
            self.Factor()

    def Factor(self):
        self._prod("<Factor> -> <Identifier> | <Number> | ( <Expression> )")
        t = self.lookahead
        if t.type == "IDENT":
            self._match("IDENT")
        elif t.type == "NUMBER":
            self._match("NUMBER")
        elif t.type == "SEP" and t.lexeme == "(":
            self._match("SEP", "(")
            self.Expression()
            self._match("SEP", ")")
        else:
            self._error({"IDENT","NUMBER","SEP('(')"})

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 parser.py <input_file> <output_file>")
        sys.exit(1)
    src_path, out_path = sys.argv[1], sys.argv[2]
    with open(src_path, "r") as f:
        text = f.read()
    with open(out_path, "w") as out:
        parser = Parser(text, out)
        try:
            parser.parse()
            print("Parsing complete: input is syntactically correct.", file=out)
        except SyntaxError as e:
            print(str(e), file=out)
            print("Parsing aborted due to syntax error.", file=out)

if __name__ == "__main__":
    main()
