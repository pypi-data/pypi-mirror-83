from parsimonious import TokenGrammar, ParseError, IncompleteParseError  # type: ignore

grammar = TokenGrammar(
    r"""
HeaderFile                 = HeaderFileElement+
HeaderFileElement          = IncludeStatement /
                             TypeDeclaration /
                             FunctionDeclaration

ImplementationFile         = ImplementationFileElement+
ImplementationFileElement  = HeaderFileElement /
                             FunctionDefinition

IncludeStatement           = "include" string_literal ";"

TypeDeclaration            = StructDeclaration /
                             EnumDeclaration /
                             TypedefDeclaration
StructDeclaration          = "struct" identifier "{" VariableDeclaration+ "}" ";"
EnumDeclaration            = "enum" identifier "{" EnumBody "}" ";"
EnumBody                   = (identifier ("=" Expression)? "," EnumBody) /
                             (identifier ("=" Expression)? ","?)
TypedefDeclaration         = "typedef" identifier "=" Type ";"

FunctionDeclaration        = FunctionSignature ";"
FunctionDefinition         = FunctionSignature Block
FunctionSignature          = Type identifier "(" SignatureArguments? ")"
SignatureArguments         = (Type identifier "," SignatureArguments) /
                             (Type identifier ","?)

Block                      = "{" Statement* "}"
       
Statement                  = VariableDefinition /
                             VariableDeclaration /
                             IfStatement /
                             SwitchStatement /
                             WhileStatement /
                             DoWhileStatement /
                             ForStatement /
                             FlowControlStatement /
                             AssignmentStatement /
                             ExpressionStatement

VariableDefinition         = Type identifier "=" Expression ";"
VariableDeclaration        = Type identifier ";"

IfStatement                = ("if" Expression Block "else" Block) /
                             ("if" Expression Block)

SwitchStatement            = "switch" Expression "{" SwitchCase+ "}"
SwitchCase                 = (CaseSpecifier Block) /
                             ("default" Block)
CaseSpecifier              = ("case" Expression "," CaseSpecifier) /
                             ("case" Expression ","?)

WhileStatement             = "while" Expression Block
DoWhileStatement           = "do" Block "while" Expression ";"
ForStatement               = "for" VariableDefinition? ";" Expression ";" AssignmentStatementBody? Block
   
FlowControlStatement       = ("continue" ";") /
                             ("break" ";") /
                             ("return" Expression? ";")
   
AssignmentStatement        = AssignmentStatementBody ";"
AssignmentStatementBody    = (AssignmentTargetExpression "=" Expression) /
                             (AssignmentTargetExpression "+=" Expression) /
                             (AssignmentTargetExpression "-=" Expression) /
                             (AssignmentTargetExpression "*=" Expression) /
                             (AssignmentTargetExpression "/=" Expression) /
                             (AssignmentTargetExpression "%=" Expression) /
                             (AssignmentTargetExpression "&=" Expression) /
                             (AssignmentTargetExpression "^=" Expression) /
                             (AssignmentTargetExpression "|=" Expression) /
                             (AssignmentTargetExpression "++") /
                             (AssignmentTargetExpression "--")

ExpressionStatement        = Expression ";"
   
Type                       = ("const" BasicType) /
                             (BasicType "*") /
                             (BasicType "[" Expression "]") /
                             (BasicType "function" "(" (BasicType ",")* ")") /
                             BasicType
BasicType                  = "void" /
                             IntegerType /
                             ("signed" IntegerType) /
                             ("unsigned" IntegerType) /
                             "float" /
                             "double" /
                             "bool" /
                             ("struct" identifier) /
                             ("enum" identifier) /
                             ("typedef" identifier) /
                             ("(" Type ")")
IntegerType                = "char" /
                             "short" /
                             "int" /
                             "long"

AssignmentTargetExpression = identifier ATEElementSuffix*
ATEElementSuffix           = ("[" Expression "]") /
                             ("." identifier) /
                             ("->" identifier)

AtomicExpression           = identifier /
                             constant /
                             string_literal /
                             ("(" Expression ")")

ObjectExpression           = (AtomicExpression ObjectSuffix*) /
                             ArrayLiteralExpression /
                             StructLiteralExpression
ObjectSuffix               = ("[" Expression "]") /
                             ("(" CommasExpressionList? ")") /
                             ("." identifier) /
                             ("->" identifier)
CommasExpressionList       = (Expression "," CommasExpressionList) /
                             (Expression ","?)
ArrayLiteralExpression     = "{" CommasExpressionList "}"
StructLiteralExpression    = "{" StructLiteralBody "}"
StructLiteralBody          = (StructLiteralElement "," StructLiteralBody?) /
                             (StructLiteralElement ","?)
StructLiteralElement       = "." identifier "=" Expression

FactorExpression           = ("(" Type ")" FactorExpression) /
                             ("&" FactorExpression) /
                             ("*" FactorExpression) /
                             ("+" FactorExpression) /
                             ("-" FactorExpression) /
                             ("~" FactorExpression) /
                             ("!" FactorExpression) /
                             ("sizeof" FactorExpression) /
                             ("sizeof" Type) /
                             ObjectExpression

TermExpression             = FactorExpression TermSuffix*
TermSuffix                 = ("*" FactorExpression) /
                             ("/" FactorExpression) /
                             ("%" FactorExpression)

ArithmeticExpression       = TermExpression ArithmeticSuffix*
ArithmeticSuffix           = ("+" TermExpression) /
                             ("-" TermExpression)

BitwiseOpExpression        = (ArithmeticExpression "<<" ArithmeticExpression) /
                             (ArithmeticExpression ">>" ArithmeticExpression) /
                             (ArithmeticExpression "^" ArithmeticExpression) /
                             (ArithmeticExpression ("&" ArithmeticExpression)+) /
                             (ArithmeticExpression ("|" ArithmeticExpression)+) /
                             ArithmeticExpression

ComparisonExpression       = (BitwiseOpExpression "==" BitwiseOpExpression) /
                             (BitwiseOpExpression "!=" BitwiseOpExpression) /
                             (BitwiseOpExpression "<=" BitwiseOpExpression) /
                             (BitwiseOpExpression ">=" BitwiseOpExpression) /
                             (BitwiseOpExpression "<" BitwiseOpExpression) /
                             (BitwiseOpExpression ">" BitwiseOpExpression) /
                             BitwiseOpExpression

Expression                 = (ComparisonExpression ("&&" ComparisonExpression)+) /
                             (ComparisonExpression ("||" ComparisonExpression)+) /
                             ComparisonExpression

identifier = "identifier"
constant = "constant"
string_literal = "string_literal"
""")


class LegibleParseError(ParseError):
    def line(self):
        return "🤷"

    def column(self):
        return "🤷"


class LegibleIncompleteParseError(IncompleteParseError):
    def line(self):
        return "🤷"

    def column(self):
        return "🤷"


def parse_from_rule(rule, tokens):
    try:
        return rule.parse(tokens)
    except IncompleteParseError as error:
        raise LegibleIncompleteParseError(error.text, error.pos, error.expr)
    except ParseError as error:
        raise LegibleParseError(error.text, error.pos, error.expr)


def parse_header(tokens):
    return parse_from_rule(grammar['HeaderFile'], tokens)


def parse_implementation(tokens):
    return parse_from_rule(grammar['ImplementationFile'], tokens)
