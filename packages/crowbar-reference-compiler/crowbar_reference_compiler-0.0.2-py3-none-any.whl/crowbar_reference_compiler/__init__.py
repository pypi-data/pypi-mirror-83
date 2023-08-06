from .parser import parse_header, parse_implementation
from .scanner import scan
from .ssagen import compile_to_ssa


def main():
    import argparse

    args = argparse.ArgumentParser(description='The reference compiler for the Crowbar programming language')
    args.add_argument('-V', '--version', action='version', version='%(prog)s 0.0.2')
    args.add_argument('-g', '--include-debug-info', action='store_true')
    args.add_argument('-S', '--stop-at-assembly', action='store_true')
    args.add_argument('-o', '--out', help='output file')
    args.add_argument('input', help='input file')

    args = args.parse_args()
    if args.out is None:
        args.out = args.input.replace('.cro', '.ssa')
    with open(args.input, 'r', encoding='utf-8') as input_file:
        input_code = input_file.read()
    tokens = scan(input_code)
    parse_tree = parse_implementation(tokens)
    ssa = compile_to_ssa(parse_tree)
    with open(args.out, 'w', encoding='utf-8') as output_file:
        output_file.write(ssa)


if __name__ == '__main__':
    main()
