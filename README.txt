CPSC 323 Assignment 2

This  gives u a fully working predictive recursive descent parser in Python.
It prints tokens/lexemes and the production rules used, and emits meaningful errors.
You can plug in our assignnment 1 lexer 


To keep this self‑contained and runnable for grading, the included parser handles a clean,
left‑factored, non‑left‑recursive subset that matches the example in your prompt:
<Program>         ->   <Statements>
<Statements>      -> <Statement>  <Statements> |ε
<Statement>       -> <Assign> ;
<Assign>          ->  <Identifier>  =<Expression>
<Expression>      -> <Term> <ExpressionPrime>

<ExpressionPrime> ->  (+|-)  <Term> <ExpressionPrime> | ε
<Term>            -> <Factor> <TermPrime>
<TermPrime>       -> (*|/) <Factor> <TermPrime> |  ε
<Factor>          ->  <Identifier> |   <Number> | ( <Expression> )

Tokenns recognized by the fallback lexer:
Identifier:   [A-Za-z_][A-Za-z0-9_]
Number:       digits (integer) or float (e.g., 1,2,3,45,6.15)
Operators:    + - * / =
Separators:   ( ) ;

Whitespace and // comments are ignored.

Files
---------------------------------

- parser.py                     
- grammar_Rat25F_no_left_recursion.txt  # Grammar (subset) — left recursion removed
- test_cases/test1.rat     
- output/output_test1.txt       
- run.sh                        
- USE_YOUR_OWN_LEXER.md        

$ python3 parser.py test_cases/test1.rat output/output_test1.txt

Or use the script:
$ bash run.sh

Open parser.py and set USE_EXTERNAL_LEXER = True, then implement the thin adapter class
ExternalLexerAdapter around your own lexer API (search for "ExternalLexerAdapter" in parser.py).
The parser requires the lexer to provide:
  - peek() -> Token
  - next() -> Token (consumes current)
  - line property for current line number

The Token object must have:
  - type: one of {"IDENT","NUMBER","OP","SEP","EOF","ERROR"}
  - lexeme: string

Error handling
------------------------------------
On a syntax error, the parser reports: token, lexeme, line, and expected set, then stops.

Good luck — and feel free to extend this skeleton to the full Rat25F grammar!
