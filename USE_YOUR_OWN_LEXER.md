# Using your Assignment 1 lexer with this parser
# ==============================================
#
# 1) Set USE_EXTERNAL_LEXER = True in parser.py
# 2) Implement the ExternalLexerAdapter class to call your lexer.
#    The adapter must provide these methods/attributes:
#       - peek() -> Token
#       - next() -> Token
#       - line (property)
#    And it expects your lexer to return a token with .type and .lexeme like:
#       type in {"IDENT","NUMBER","OP","SEP","EOF","ERROR"}; lexeme is a string.
#
# 3) If your token type names differ, map them inside ExternalLexerAdapter._convert().
#
# 4) Run: python3 parser.py <input> <output>
#
# Tip: Keep PRINT_TOKENS/PRINT_PRODUCTIONS True while debugging; turn off before final hand-in if requested.
