from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser
from main import ArithmeticVisitor

def run_test(visitor, expression):
    """Executa uma expressão e retorna o resultado ou o erro."""
    try:
        lexer = ArithmeticLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = ArithmeticParser(stream)
        tree = parser.stmt()
        result = visitor.visit(tree)
        return result
    except Exception as e:
        return f"Erro: {e}"

def main():
    visitor = ArithmeticVisitor()
    tests = [
        # Testes básicos de atribuição e expressões
        {"input": "x = 5", "expected": 5},
        {"input": "y = x + 3", "expected": 8},
        {"input": "y * 2", "expected": 16},

        # Testes de comparação
        {"input": "x < 10", "expected": True},
        {"input": "x > 10", "expected": False},

        # Testes de blocos
        {"input": "{x = 10 y = 20 x + y}", "expected": 30},

        # Testes de loops
        {"input": "x = 0", "expected": 0},
        {"input": "while (x < 5) { x = x + 1 }", "expected": "Loop concluído após 5 iterações."},
        {"input": "x", "expected": 5},

        # Testes de funções
        {"input": "fun quadrado(n) { n * n }", "expected": None},
        {"input": "quadrado(4)", "expected": 16},
        {"input": "fun soma(a, b) { a + b }", "expected": None},
        {"input": "soma(3, 7)", "expected": 10},

        # Testes de condicionais
        {"input": "if (x == 5) { x + 10 } else { x - 10 }", "expected": 15},
        {"input": "if (x > 5) { x + 10 } else { x - 10 }", "expected": -5},
    ]

    print("Iniciando testes...\n")
    for i, test in enumerate(tests):
        result = run_test(visitor, test["input"])
        status = "PASSOU" if result == test["expected"] else "FALHOU"
        print(f"Teste {i + 1}: {test['input']}")
        print(f"Esperado: {test['expected']}, Obtido: {result} -> {status}\n")

if __name__ == "__main__":
    main()