import ctypes
import sys

from llvmlite import ir, binding
from ctypes import CFUNCTYPE
import json

def generate_const(ast_const):
    glob_const = {}
    for const in ast_const:
        if isinstance(ast_const[const], float):
            glob_const[const] = ir.GlobalVariable(module, ir.DoubleType(), name=const)
            glob_const[const].initializer = ir.Constant(ir.DoubleType(), ast_const[const])
        elif isinstance(ast_const[const], int):
            glob_const[const] = ir.GlobalVariable(module, ir.IntType(32), name=const)
            glob_const[const].initializer = ir.Constant(ir.IntType(32), ast_const[const])
    return glob_const

def generate_var(ast_var):
    glob_var = {}
    for var in ast_var:
        if ast_var[var] == 'int':
            glob_var[var] = ir.GlobalVariable(module, ir.IntType(32), name=var)
        elif ast_var[var] == 'real':
            glob_var[var] = ir.GlobalVariable(module, ir.DoubleType(), name=var)
    return glob_var

def generate_proc_var(builder, ast_var):
    proc_var = {}
    for var in ast_var:
        if ast_var[var] == 'int':
            proc_var[var] = builder.alloca(ir.IntType(32), name=var)
        elif ast_var[var] == 'real':
            proc_var[var] = builder.alloca(ir.DoubleType(), name=var)
    return proc_var

def generate_proc_const(builder, ast_const):
    proc_const = {}
    for const in ast_const:
        if isinstance(ast_const[const], float):
            value = ir.Constant(ir.DoubleType(), ast_const[const])
            proc_const[const] = builder.alloca(ir.DoubleType(), name=const)
            builder.store(value, proc_const[const])
        elif isinstance(ast_const[const], int):
            value = ir.Constant(ir.IntType(32), ast_const[const])
            proc_const[const] = builder.alloca(ir.IntType(32), name=const)
            builder.store(value, proc_const[const])
    return proc_const

def generate_procedure(ast, global_const, global_var, ast_var, ast_proc_var):
    for procedure in ast:
        # Создание функции
        func_type = ir.FunctionType(ir.VoidType(), [])
        func = ir.Function(module, func_type, name=procedure)
        block = func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        proc_const = generate_proc_const(builder, ast[procedure]['CONST']) if 'CONST' in ast[procedure] else None
        proc_var = generate_proc_var(builder, ast[procedure]['VAR']) if 'VAR' in ast[procedure] else None

        generate_block(builder, ast[procedure]['BLOCK'], global_const, global_var, proc_const, proc_var, ast_var, ast_proc_var)

        builder.ret_void()
    return proc_const, proc_var
    # sys.exit()

def generate_block(builder, ast, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var):
    statements = list(ast.keys())
    for statement in statements:
        if 'assign' == statement:
            generate_assign(builder, ast['assign'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        elif 'write' == statement:
            value = generate_expression(builder, ast['write'], all_const, all_var, proc_const, proc_var,)
            create_print_function(builder, value)
        elif 'ifthen' == statement:
            builder = generate_ifthen(builder, ast['ifthen'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        elif 'ifthenelse' == statement:
            builder = generate_ifthenelse(builder, ast['ifthenelse'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        elif 'whiledo' == statement:
            builder = generate_whiledo(builder, ast['whiledo'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        elif 'call' == statement:
            generate_call(builder, ast['call'])

    return builder

def generate_call(builder, ast_call):
    procedure = module.declare_intrinsic(ast_call['id'])
    builder.call(procedure, [])

def exp_type(builder, left, right):
    if left.type == ir.IntType(32):
        if right.type == ir.IntType(32):
            return int, left, right
        elif right.type == ir.DoubleType():
            left = builder.sitofp(left, ir.DoubleType())
            return float, left, right
    elif left.type == ir.DoubleType():
        if right.type == ir.IntType(32):
            right = builder.sitofp(right, ir.DoubleType())
            return float, left, right
        elif right.type == ir.DoubleType():
            return float, left, right

def print_llvm(builder, value, printf_func):
    if value.type == ir.IntType(32):
        format_str = "%d\n\0"
    elif value.type == ir.DoubleType():
        format_str = "%f\n\0"
    format_str_array = ir.ArrayType(ir.IntType(8), len(format_str))
    format_str_ptr = builder.alloca(format_str_array)
    format_str_const = ir.Constant(format_str_array, bytearray(format_str.encode("utf-8")))
    builder.store(format_str_const, format_str_ptr)
    builder.call(printf_func, [builder.bitcast(format_str_ptr, ir.IntType(8).as_pointer()), value])

def create_print_function(builder, value):
    if any(func.name == 'printf' for func in module.functions):
        printf_func = module.declare_intrinsic('printf')
    else:
        printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        printf_func = ir.Function(module, printf_type, name='printf')
    print_llvm(builder, value, printf_func)

def generate_assign(builder, assign, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var):
    id = assign['id']
    value = generate_expression(builder, assign['expression'], all_const, all_var, proc_const, proc_var)
    try:
        if ast_var[id] == 'int':
            if value.type == ir.IntType(32):
                result = builder.store(value, global_var[id])
            else:
                print(f'Тип значения не подходит переменной {id}, должен быть i32')
                sys.exit()
        elif ast_var[id] == 'real':
            if value.type == ir.DoubleType():
                result = builder.store(value, global_var[id])
            else:
                print(f'Тип значения не подходит переменной {id}, должен быть double')
                sys.exit()
    except:
        for proc in ast_proc_var:
            if ast_proc_var[proc][id] == 'int':
                if value.type == ir.IntType(32):
                    result = builder.store(value, proc_var[id])
                else:
                    print(f'Тип значения не подходит переменной {id}, должен быть i32')
                    sys.exit()
            elif ast_proc_var[proc][id] == 'real':
                if value.type == ir.DoubleType():
                    result = builder.store(value, proc_var[id])
                else:
                    print(f'Тип значения не подходит переменной {id}, должен быть double')
                    sys.exit()
    return result

def generate_ifthen(builder, ast_ifthen, all_const, all_var, proc_const, proc_var, ast_var,ast_proc_var):
    condition = generate_condition(builder, ast_ifthen['condition'], all_const, all_var, proc_const, proc_var)
    # Создание блока "then"
    then_block = builder.append_basic_block("then")
    if_builder = ir.IRBuilder(then_block)
    after_if_block = builder.append_basic_block("after_if")
    after_if_builder = ir.IRBuilder(after_if_block)
    # Переход к блоку на основании сравнения
    builder.cbranch(condition, then_block, after_if_block)
    generate_block(if_builder, ast_ifthen['if_body'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    builder.position_at_end(after_if_block)
    # переход в основной блок
    if_builder.branch(after_if_block)
    return after_if_builder

def generate_ifthenelse(builder, ast_ifthenelse, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var):
    condition = generate_condition(builder, ast_ifthenelse['condition'], all_const, all_var, proc_const, proc_var)
    ast_ifthen = ast_ifthenelse['if_body']
    ast_ifelse = ast_ifthenelse['else_body']
    # Создание блока "then"
    then_block = builder.append_basic_block("if_then")
    then_builder = ir.IRBuilder(then_block)
    else_block = builder.append_basic_block("else")
    else_builder = ir.IRBuilder(else_block)
    after_if_block = builder.append_basic_block("after_ifelse")
    after_if_builder = ir.IRBuilder(after_if_block)
    # Переход к блоку на основании сравнения
    builder.cbranch(condition, then_block, else_block)
    # Код, который должен выполняться в блоке "then"
    if len(ast_ifthenelse['if_body']) > 1:
        if_body = list(ast_ifthen.items())[:-1]
        ast_thenbody = {}
        for element, value in if_body:
            ast_thenbody[element] = value
        generate_block(then_builder, ast_thenbody, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        element, value = list(ast_ifthen.items())[-1]
        then_result = generate_block(then_builder, {element:value}, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    elif len(ast_ifthen) == 1:
        then_result = generate_block(then_builder, ast_ifthen, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    # переход в основной блок
    then_builder.branch(after_if_block)

    # Код, который должен выполняться в блоке "else"
    if len(ast_ifthenelse['else_body']) > 1:
        else_body = list(ast_ifelse.items())[:-1]
        ast_elsebody = {}
        for element, value in else_body:
            ast_elsebody[element] = value
        generate_block(else_builder, ast_elsebody, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
        element, value = list(ast_ifelse.items())[-1]
        else_result = generate_block(else_builder, {element: value}, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    elif len(ast_ifelse) == 1:
        else_result = generate_block(else_builder, ast_ifelse, all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    # переход в основной блок
    else_builder.branch(after_if_block)
    # Код, который должен выполняться после "then" или "else"
    builder.position_at_end(after_if_block)
    return after_if_builder

def generate_condition(builder, ast_condition, all_const, all_var, proc_const, proc_var):
    left = generate_expression(builder, ast_condition['left'], all_const, all_var, proc_const, proc_var)
    right = generate_expression(builder, ast_condition['right'], all_const, all_var, proc_const, proc_var)
    cond_type, left, right = exp_type(builder, left, right)
    if cond_type == int:
        return builder.icmp_signed(ast_condition['op'], left, right)
    elif cond_type == float:
        return builder.fcmp_ordered(ast_condition['op'], left, right)

def generate_number(value):
    if isinstance(value, float):
        return ir.Constant(ir.DoubleType(), value)
    if isinstance(value, int):
        return ir.Constant(ir.IntType(32), value)

def generate_id(builder, id, consts, vars, proc_const, proc_var):
    if id in consts:
        value = builder.load(consts[id])
    elif id in vars:
        value = builder.load(vars[id])
    elif id in proc_var:
        value = builder.load(proc_var[id])
    elif id in proc_const:
        value = builder.load(proc_const[id])
    return value

def generate_add(builder, left, right):
    args_type, arg1, arg2 = exp_type(builder, left, right)
    if args_type == float:
        return builder.fadd(arg1, arg2)
    elif args_type == int:
        return builder.add(arg1, arg2)
def generate_sub(builder, left, right):
    args_type, arg1, arg2 = exp_type(builder, left, right)
    if args_type == float:
        return builder.fsub(arg1, arg2)
    elif args_type == int:
        return builder.sub(arg1, arg2)
def generate_mul(builder, left, right):
    args_type, arg1, arg2 = exp_type(builder, left, right)
    if args_type == float:
        return builder.fmul(arg1, arg2)
    elif args_type == int:
        return builder.mul(arg1, arg2)
def generate_div(builder, left, right):
    args_type, arg1, arg2 = exp_type(builder, left, right)
    if args_type == float:
        return builder.fdiv(arg1, arg2)
    elif args_type == int:
        return builder.sdiv(arg1, arg2)

def generate_expression(builder, expr, consts, vars, proc_const, proc_var):
    if 'number' in expr:
        return generate_number(expr['number'])
    elif 'op' in expr:
        arg1 = generate_expression(builder, expr['left'], consts, vars, proc_const, proc_var,)
        arg2 = generate_expression(builder, expr['right'], consts, vars, proc_const, proc_var,)
        if expr['op'] == '+':
            return generate_add(builder, arg1, arg2)
        elif expr['op'] == '-':
            return generate_sub(builder, arg1, arg2)
        elif expr['op'] == '*':
            return generate_mul(builder, arg1, arg2)
        elif expr['op'] == '/':
            return generate_div(builder, arg1, arg2)
    elif 'id' in expr:
        return generate_id(builder, expr['id'], consts, vars, proc_const, proc_var)
    else:
        raise ValueError(f"Unknown expression type: {expr}")

def generate_whiledo(builder, ast_whiledo, all_const, all_var, proc_const, proc_var, ast_var,ast_proc_var):
    # Создание блоков "whiledo"
    while_condition_block = builder.append_basic_block("while_condition")
    while_condition_builder = ir.IRBuilder(while_condition_block)
    whiledo_block = builder.append_basic_block("whiledo")
    whiledo_builder = ir.IRBuilder(whiledo_block)
    after_whiledo_block = builder.append_basic_block("after_whiledo")
    after_whiledo_builder = ir.IRBuilder(after_whiledo_block)
    # проверка условия
    # builder.goto_block(while_condition_block)
    builder.branch(while_condition_block)
    condition = generate_condition(while_condition_builder, ast_whiledo['condition'], all_const, all_var, proc_const, proc_var)
    # Переход к блоку на основании сравнения
    while_condition_builder.cbranch(condition, whiledo_block, after_whiledo_block)

    generate_block(whiledo_builder, ast_whiledo['while_body'], all_const, all_var, proc_const, proc_var, ast_var, ast_proc_var)
    whiledo_builder.branch(while_condition_block)

    return after_whiledo_builder


# AST
with open("ast.json", "r") as f:
    ast = json.load(f)

# Создание LLVM-модуля
module = ir.Module(name='llvm')
try:
    global_const = generate_const(ast['CONST'])
except:
    global_const = None
try:
    global_var = generate_var(ast['VAR'])
except:
    global_var = None

ast_proc_var = {}
try:
    for procedure in ast['PROCEDURES']:
        try:
            ast_proc_var[procedure] = {}
            for var in ast['PROCEDURES'][procedure]['VAR']:
                ast_proc_var[procedure][var] = ast['PROCEDURES'][procedure]['VAR'][var]
        except:
            print(f"В процедуре {procedure} нет локальных переменных")

    proc_const, proc_var = generate_procedure(ast['PROCEDURES'], global_const, global_var, ast['VAR'], ast_proc_var)
except:
    print('Нет процедур')
    proc_const, proc_var = None, None

# Создание функции
func_type = ir.FunctionType(ir.VoidType(), [])
func = ir.Function(module, func_type, name="main")
block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

builder = generate_block(builder, ast['BLOCK'], global_const, global_var, proc_const, proc_var, ast['VAR'], ast_proc_var)

builder.ret_void()

# Получение строкового представления модуля LLVM
llvm_ir = str(module)

# Вывод LLVM-кода в файл
with open("llvm_code.txt", "w") as f:
    f.write(llvm_ir)
print("LLVM-код сохранен в файле 'llvm_code.txt'.")