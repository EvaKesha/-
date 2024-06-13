# Generated from C:/Users/Evgenia/Desktop/Курсовая работа/expl0.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .expl0Parser import expl0Parser
else:
    from expl0Parser import expl0Parser

# This class defines a complete listener for a parse tree produced by expl0Parser.
class expl0Listener(ParseTreeListener):

    # Enter a parse tree produced by expl0Parser#program.
    def enterProgram(self, ctx:expl0Parser.ProgramContext):
        pass

    # Exit a parse tree produced by expl0Parser#program.
    def exitProgram(self, ctx:expl0Parser.ProgramContext):
        pass


    # Enter a parse tree produced by expl0Parser#const.
    def enterConst(self, ctx:expl0Parser.ConstContext):
        pass

    # Exit a parse tree produced by expl0Parser#const.
    def exitConst(self, ctx:expl0Parser.ConstContext):
        pass


    # Enter a parse tree produced by expl0Parser#var.
    def enterVar(self, ctx:expl0Parser.VarContext):
        pass

    # Exit a parse tree produced by expl0Parser#var.
    def exitVar(self, ctx:expl0Parser.VarContext):
        pass


    # Enter a parse tree produced by expl0Parser#procedure.
    def enterProcedure(self, ctx:expl0Parser.ProcedureContext):
        pass

    # Exit a parse tree produced by expl0Parser#procedure.
    def exitProcedure(self, ctx:expl0Parser.ProcedureContext):
        pass


    # Enter a parse tree produced by expl0Parser#block.
    def enterBlock(self, ctx:expl0Parser.BlockContext):
        pass

    # Exit a parse tree produced by expl0Parser#block.
    def exitBlock(self, ctx:expl0Parser.BlockContext):
        pass


    # Enter a parse tree produced by expl0Parser#statement.
    def enterStatement(self, ctx:expl0Parser.StatementContext):
        pass

    # Exit a parse tree produced by expl0Parser#statement.
    def exitStatement(self, ctx:expl0Parser.StatementContext):
        pass


    # Enter a parse tree produced by expl0Parser#assign.
    def enterAssign(self, ctx:expl0Parser.AssignContext):
        pass

    # Exit a parse tree produced by expl0Parser#assign.
    def exitAssign(self, ctx:expl0Parser.AssignContext):
        pass


    # Enter a parse tree produced by expl0Parser#expression.
    def enterExpression(self, ctx:expl0Parser.ExpressionContext):
        pass

    # Exit a parse tree produced by expl0Parser#expression.
    def exitExpression(self, ctx:expl0Parser.ExpressionContext):
        pass


    # Enter a parse tree produced by expl0Parser#call.
    def enterCall(self, ctx:expl0Parser.CallContext):
        pass

    # Exit a parse tree produced by expl0Parser#call.
    def exitCall(self, ctx:expl0Parser.CallContext):
        pass


    # Enter a parse tree produced by expl0Parser#write.
    def enterWrite(self, ctx:expl0Parser.WriteContext):
        pass

    # Exit a parse tree produced by expl0Parser#write.
    def exitWrite(self, ctx:expl0Parser.WriteContext):
        pass


    # Enter a parse tree produced by expl0Parser#ifthen.
    def enterIfthen(self, ctx:expl0Parser.IfthenContext):
        pass

    # Exit a parse tree produced by expl0Parser#ifthen.
    def exitIfthen(self, ctx:expl0Parser.IfthenContext):
        pass


    # Enter a parse tree produced by expl0Parser#ifthenelse.
    def enterIfthenelse(self, ctx:expl0Parser.IfthenelseContext):
        pass

    # Exit a parse tree produced by expl0Parser#ifthenelse.
    def exitIfthenelse(self, ctx:expl0Parser.IfthenelseContext):
        pass


    # Enter a parse tree produced by expl0Parser#whiledo.
    def enterWhiledo(self, ctx:expl0Parser.WhiledoContext):
        pass

    # Exit a parse tree produced by expl0Parser#whiledo.
    def exitWhiledo(self, ctx:expl0Parser.WhiledoContext):
        pass


    # Enter a parse tree produced by expl0Parser#condition.
    def enterCondition(self, ctx:expl0Parser.ConditionContext):
        pass

    # Exit a parse tree produced by expl0Parser#condition.
    def exitCondition(self, ctx:expl0Parser.ConditionContext):
        pass


    # Enter a parse tree produced by expl0Parser#float_number.
    def enterFloat_number(self, ctx:expl0Parser.Float_numberContext):
        pass

    # Exit a parse tree produced by expl0Parser#float_number.
    def exitFloat_number(self, ctx:expl0Parser.Float_numberContext):
        pass



del expl0Parser