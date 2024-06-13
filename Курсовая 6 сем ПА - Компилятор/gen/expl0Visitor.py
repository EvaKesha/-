# Generated from C:/Users/Evgenia/Desktop/Курсовая работа/expl0.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .expl0Parser import expl0Parser
else:
    from expl0Parser import expl0Parser

# This class defines a complete generic visitor for a parse tree produced by expl0Parser.

class expl0Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by expl0Parser#program.
    def visitProgram(self, ctx:expl0Parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#const.
    def visitConst(self, ctx:expl0Parser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#var.
    def visitVar(self, ctx:expl0Parser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#procedure.
    def visitProcedure(self, ctx:expl0Parser.ProcedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#block.
    def visitBlock(self, ctx:expl0Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#statement.
    def visitStatement(self, ctx:expl0Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#assign.
    def visitAssign(self, ctx:expl0Parser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#expression.
    def visitExpression(self, ctx:expl0Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#call.
    def visitCall(self, ctx:expl0Parser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#write.
    def visitWrite(self, ctx:expl0Parser.WriteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#ifthen.
    def visitIfthen(self, ctx:expl0Parser.IfthenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#ifthenelse.
    def visitIfthenelse(self, ctx:expl0Parser.IfthenelseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#whiledo.
    def visitWhiledo(self, ctx:expl0Parser.WhiledoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#condition.
    def visitCondition(self, ctx:expl0Parser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expl0Parser#float_number.
    def visitFloat_number(self, ctx:expl0Parser.Float_numberContext):
        return self.visitChildren(ctx)



del expl0Parser