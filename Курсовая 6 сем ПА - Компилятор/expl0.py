import sys

import antlr4
import json
from gen.expl0Lexer import expl0Lexer
from gen.expl0Parser import expl0Parser
from gen.expl0Visitor import expl0Visitor

class MyVisitor(expl0Visitor):
    def __init__(self):
        self.ast = {}

    def visitProgram(self, ctx: expl0Parser.ProgramContext):
        if ctx.main_const:
            self.ast['CONST'] = self.visitConst(ctx.main_const)
        if ctx.main_var:
            self.ast['VAR'] = self.visitVar(ctx.main_var)
        if ctx.procedure():
            self.ast['PROCEDURES'] = {}
            for procedure_ctx in ctx.procedure():
                procedure_id, procedure_tree = self.visitProcedure(procedure_ctx)
                self.ast['PROCEDURES'][procedure_id] = procedure_tree
        if ctx.block():
            self.ast['BLOCK'] = self.visitBlock(ctx.block())
        return self.ast

    def visitConst(self, ctx: expl0Parser.ConstContext):
        all_const = ctx.getText().replace('const', '').replace('CONST', '').replace(';', '').split(',')
        const_tree = {}
        for decl in all_const:
            key, value = decl.split('=')
            try:
                const_tree[key] = int(value)
            except:
                const_tree[key] = float(value)
        return const_tree

    def visitVar(self, ctx: expl0Parser.VarContext):
        all_var = ctx.getText().replace('var', '').replace('VAR', '').split(';')
        var_tree = {}
        if 'integer' in all_var[0]:
            int_var = all_var[0].replace(':integer', '')
            int_var = int_var.split(',')
            if 'real' in all_var[1]:
                real_var = all_var[1].replace(':real', '')
                real_var = real_var.split(',')
        elif 'integer' in all_var[1]:
            int_var = all_var[1].replace(':integer', '')
            int_var = int_var.split(',')
            if 'real' in all_var[0]:
                real_var = all_var[0].replace(':real', '')
                real_var = real_var.split(',')
        try:
            for var in int_var:
                var_tree[var] = 'int'
        except:
            print('Нет переменных типа integer')
        try:
            for var in real_var:
                var_tree[var] = 'real'
        except:
            print('Нет переменных типа real')
        return var_tree

    def visitProcedure(self, ctx: expl0Parser.ProcedureContext):
        procedure_tree = {}
        if ctx.proc_const:
            procedure_tree['CONST'] = self.visitConst(ctx.proc_const)
        if ctx.proc_var:
            procedure_tree['VAR'] = self.visitVar(ctx.proc_var)
        if ctx.block():
            procedure_tree['BLOCK'] = self.visitBlock(ctx.block())
        return ctx.procedure_id.text, procedure_tree

    def visitBlock(self, ctx: expl0Parser.BlockContext):
        block_tree = {}
        for statement_ctx in ctx.statement():
            element, value = self.visitStatement(statement_ctx)
            block_tree[element] = value
        return block_tree

    def visitStatement(self, ctx: expl0Parser.StatementContext):
        if ctx.assign():
            return 'assign', self.visitAssign(ctx.assign())
        elif ctx.call():
            return 'call', self.visitCall(ctx.call())
        elif ctx.ifthen():
            return 'ifthen', self.visitIfthen(ctx.ifthen())
        elif ctx.ifthenelse():
            return 'ifthenelse', self.visitIfthenelse(ctx.ifthenelse())
        elif ctx.whiledo():
            return 'whiledo', self.visitWhiledo(ctx.whiledo())
        elif ctx.write():
            return 'write', self.visitWrite(ctx.write())

    def visitAssign(self, ctx: expl0Parser.AssignContext):
        return {'id': ctx.ID().getText(), 'expression': self.visitExpression(ctx.expression())}

    def visitCall(self, ctx: expl0Parser.CallContext):
        return {'id': ctx.ID().getText()}

    def visitIfthen(self, ctx: expl0Parser.IfthenContext):
        if ctx.if_body:
            if_body = self.visitBlock(ctx.if_body)
        else:
            element, value = self.visitStatement(ctx.statement())
            if_body = {element: value}
        return {'condition': self.visitCondition(ctx.condition()), 'if_body': if_body}

    def visitIfthenelse(self, ctx: expl0Parser.IfthenelseContext):
        if ctx.if_body:
            if_body = self.visitBlock(ctx.if_body)
        else:
            element, value = self.visitStatement(ctx.if_st)
            if_body = {element: value}
        if ctx.else_body:
            else_body = self.visitBlock(ctx.else_body)
        else:
            element, value = self.visitStatement(ctx.else_st)
            else_body = {element: value}
        return {'condition': self.visitCondition(ctx.condition()), 'if_body': if_body, 'else_body': else_body}

    def visitWhiledo(self, ctx: expl0Parser.WhiledoContext):
        if ctx.while_body:
            while_body = self.visitBlock(ctx.while_body)
        else:
            element, value = self.visitStatement(ctx.statement())
            while_body = {element: value}
        return {'condition': self.visitCondition(ctx.condition()), 'while_body': while_body}

    def visitWrite(self, ctx: expl0Parser.WriteContext):
        if ctx.ID():
            return {'id': ctx.ID().getText()}
        elif ctx.NUMBER():
            return {'number': int(ctx.NUMBER().getText())}
        elif ctx.float_number():
            return {'number': float(ctx.float_number().getText())}

    def visitExpression(self, ctx: expl0Parser.ExpressionContext):
        if ctx.ID():
            return {'id': ctx.ID().getText()}
        elif ctx.NUMBER():
            return {'number': int(ctx.NUMBER().getText())}
        elif ctx.float_number():
            return {'number': float(ctx.float_number().getText())}
        elif ctx.left and ctx.right and ctx.op:
            return {
                'left': self.visitExpression(ctx.left),
                'right': self.visitExpression(ctx.right),
                'op': ctx.op.text
            }
        else:
            raise ValueError(f"Unexpected expression context: {ctx.getText()}")

    def visitCondition(self, ctx: expl0Parser.ConditionContext):
        return {
            'left': self.visitExpression(ctx.left),
            'right': self.visitExpression(ctx.right),
            'op': ctx.op.text
        }

# Usage
input_text = open('ex1.txt', 'r').read()
lexer = expl0Lexer(antlr4.InputStream(input_text))
stream = antlr4.CommonTokenStream(lexer)
parser = expl0Parser(stream)
tree = parser.program()
visitor = MyVisitor()
ast = visitor.visitProgram(tree)

with open('ast.json', 'w') as f:
    json.dump(ast, f, indent=2)
