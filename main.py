from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    def __init__(self):
        # Ambiente para armazenar variáveis e funções
        self.env = {}

    def visit(self, ctx):
        """Método principal para visitar nós da árvore de sintaxe."""
        if isinstance(ctx, TerminalNode):
            return ctx.getText()

        rule = ctx.getRuleIndex()
        visit_methods = {
            ArithmeticParser.RULE_assignment: self.visitAssignment,
            ArithmeticParser.RULE_ifStmt: self.visitIfStmt,
            ArithmeticParser.RULE_whileStmt: self.visitWhileStmt,
            ArithmeticParser.RULE_funcDef: self.visitFuncDef,
            ArithmeticParser.RULE_block: self.visitBlock,
            ArithmeticParser.RULE_expr: self.visitExpr,
            ArithmeticParser.RULE_term: self.visitTerm,
            ArithmeticParser.RULE_factor: self.visitFactor,
            ArithmeticParser.RULE_atom: self.visitAtom,
            ArithmeticParser.RULE_functionCall: self.visitFunctionCall,
            ArithmeticParser.RULE_comparison: self.visitComparison,
        }

        if rule in visit_methods:
            return visit_methods[rule](ctx)

        # Caso não seja uma regra específica, visita os filhos
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        result = None
        for child in ctx.getChildren():
            result = self.visit(child)
        return result

    def visitAssignment(self, ctx):
        """Processa atribuições de variáveis."""
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.env[var_name] = value
        return value

    def visitIfStmt(self, ctx):
        """Processa declarações condicionais (if/else)."""
        condition = self.visit(ctx.comparison())
        if condition:
            return self.visit(ctx.stmt(0))
        elif ctx.ELSE():
            return self.visit(ctx.stmt(1))
        return None

    def visitWhileStmt(self, ctx):
        """Processa loops while."""
        max_iterations = 1000
        iterations = 0

        while self.visit(ctx.comparison()):
            if iterations >= max_iterations:
                raise RuntimeError("Loop infinito detectado no 'while'")
            self.visit(ctx.block())
            iterations += 1

        return f"Loop concluído após {iterations} iterações."

    def visitFuncDef(self, ctx):
        """Processa definições de funções."""
        func_name = ctx.VAR().getText()
        params = [v.getText() for v in ctx.paramList().getChildren() if v.getText().isalpha()] if ctx.paramList() else []
        body = ctx.stmt()
        self.env[func_name] = ("function", params, body)
        return None

    def visitFunctionCall(self, ctx):
        """Processa chamadas de funções."""
        func_name = ctx.VAR().getText()
        if func_name not in self.env:
            raise ValueError(f"Função não definida: {func_name}")

        func_def = self.env[func_name]
        if not (isinstance(func_def, tuple) and func_def[0] == "function"):
            raise ValueError(f"{func_name} não é uma função")

        params, body = func_def[1], func_def[2]
        args = [self.visit(child) for child in ctx.argList().getChildren() if child.getText() != ','] if ctx.argList() else []

        if len(params) != len(args):
            raise ValueError("Número de argumentos incompatível")

        old_env = self.env.copy()
        for i in range(len(params)):
            self.env[params[i]] = args[i]

        result = self.visit(body)
        self.env = old_env
        return result

    def visitBlock(self, ctx):
        """Processa blocos de código."""
        result = None
        for stmt in ctx.stmt():
            result = self.visit(stmt)
        return result

    def visitExpr(self, ctx):
        """Processa expressões aritméticas."""
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.expr())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.term())
        return left + right if op == '+' else left - right

    def visitTerm(self, ctx):
        """Processa termos aritméticos."""
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.term())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.factor())
        return left * right if op == '*' else left / right

    def visitFactor(self, ctx):
        """Processa fatores (chamadas de função ou átomos)."""
        if ctx.functionCall():
            return self.visit(ctx.functionCall())
        elif ctx.atom():
            return self.visit(ctx.atom())
        raise ValueError("Contexto inesperado em visitFactor")

    def visitAtom(self, ctx):
        """Processa átomos (números, variáveis ou expressões entre parênteses)."""
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.env:
                return self.env[var_name]
            raise ValueError(f"Variável não definida: {var_name}")
        return self.visit(ctx.expr())

    def visitComparison(self, ctx):
        """Processa comparações."""
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        operations = {
            '<': left < right,
            '<=': left <= right,
            '>': left > right,
            '>=': left >= right,
            '==': left == right,
            '!=': left != right,
        }
        if op in operations:
            return operations[op]
        raise ValueError(f"Operador desconhecido: {op}")

def main():
    """Função principal para executar o REPL."""
    visitor = ArithmeticVisitor()
    print("Digite 'exit' ou 'quit' para sair.")
    while True:
        try:
            expression = input(">>> ")
            if expression.strip().lower() in {"exit", "quit"}:
                break
            if not expression.strip():
                continue

            lexer = ArithmeticLexer(InputStream(expression))
            stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(stream)
            tree = parser.stmt()
            result = visitor.visit(tree)

            if result is not None:
                print("Resultado:", result)
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    main()
