from parsimonious import NodeVisitor  # type: ignore
from parsimonious.nodes import Node  # type: ignore


class SsaGenVisitor(NodeVisitor):
    def __init__(self):
        self.data = []

    def visit_ImplementationFile(self, node, visited_children):
        data = '\n'.join(self.data)
        functions = '\n'.join(visited_children)
        return data + '\n' + functions

    def visit_IncludeStatement(self, node, visited_children):
        include, included_header, semicolon = visited_children
        assert include.text[0].type == 'include'
        assert included_header.type == 'string_literal'
        included_header = included_header.data
        assert semicolon.text[0].type == ';'
        print("including", included_header)
        return ''

    def visit_FunctionDefinition(self, node, visited_children):
        signature, body = visited_children
        return_type, name, args = signature
        body = '\n'.join('    ' + instr for instr in body)
        return f"export function w ${name}() {{\n@start\n{body}\n}}"

    def visit_FunctionSignature(self, node, visited_children):
        return_type, name, lparen, args, rparen = visited_children
        assert name.type == 'identifier'
        name = name.data
        assert lparen.text[0].type == '('
        assert rparen.text[0].type == ')'
        return return_type, name, args

    def visit_Block(self, node, visited_children):
        lbrace, statements, rbrace = visited_children
        return statements

    def visit_Statement(self, node, visited_children):
        return visited_children[0]

    def visit_ExpressionStatement(self, node, visited_children):
        expression, semicolon = visited_children
        assert semicolon.text[0].type == ';'
        return expression

    def visit_Expression(self, node, visited_children):
        # TODO handle logical and/or
        return visited_children[0]

    def visit_ComparisonExpression(self, node, visited_children):
        # TODO handle comparisons
        return visited_children[0]

    def visit_BitwiseOpExpression(self, node, visited_children):
        # TODO handle bitwise operations
        return visited_children[0]

    def visit_ArithmeticExpression(self, node, visited_children):
        # TODO handle addition/subtraction
        return visited_children[0]

    def visit_TermExpression(self, node, visited_children):
        # TODO handle multiplication/division/modulus
        return visited_children[0]

    def visit_FactorExpression(self, node, visited_children):
        # TODO handle casts/address-of/pointer-dereference/unary ops/sizeof
        return visited_children[0]

    def visit_ObjectExpression(self, node, visited_children):
        # TODO handle array literals
        # TODO handle struct literals
        base, suffices = visited_children[0]
        if isinstance(suffices, Node):
            suffices = suffices.children
        if len(suffices) == 0:
            return base
        if base.type == 'identifier' and suffices[0].text[0].type == '(':
            arguments = suffices[1]
            if arguments[0].type == 'string_literal':
                data = arguments[0].data
                name = f"$data{len(self.data)}"
                # TODO handle non-variadic functions
                arguments = [f"l {name}", '...']
                self.data.append(f"data {name} = {{ b {data}, b 0 }}")
            return f"call ${base.data}({', '.join(arguments)})"
        print(base)
        print(suffices[0])

    def visit_AtomicExpression(self, node, visited_children):
        # TODO handle parenthesized subexpressions
        return visited_children[0]

    def visit_FlowControlStatement(self, node, visited_children):
        # TODO handle break/continue
        ret, arg, semicolon = visited_children[0]
        assert ret.text[0].type == 'return'
        assert semicolon.text[0].type == ';'
        if arg.type == 'constant':
            return f"ret {arg.data}"

    def visit_constant(self, node, visited_children):
        return node.text[0]

    def visit_string_literal(self, node, visited_children):
        return node.text[0]

    def visit_identifier(self, node, visited_children):
        return node.text[0]

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        if not visited_children:
            return node
        if len(visited_children) == 1:
            return visited_children[0]
        return visited_children


def compile_to_ssa(parse_tree):
    ssa_gen = SsaGenVisitor()
    return ssa_gen.visit(parse_tree)
