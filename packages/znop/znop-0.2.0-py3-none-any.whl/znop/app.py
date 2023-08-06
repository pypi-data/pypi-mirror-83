import sys
import json
from pathlib import Path
from znop.core import ZnEquation, ZnExpression
from znop.exceptions import ParseError, ResolveError


db_filepath = ""

db = {}

n = 10

help_info = """
    set n=<setnumber>   | Set the set number of Z
    reduce <expression> | Reduce a Zn expression or equation
    solve <equation>    | Solve an one-dimensional Zn equation
    help                | Usage of this program
    quit                | Quit this program"""

def input_save(prompt: str):
    input_str = input(prompt)
    if "quit" != input_str[:4]:
        db["history"].append(prompt + input_str)
    return input_str

def print_save(*line):
    print(*line)
    line = ' '.join([str(l) for l in line])
    db["history"].append(line)
    if len(db["history"]) > 300:
        db["history"] = db["history"][-200:]

def quit_app():
    if len(db["history"]) > 200:
        db["history"] = db["history"][-200:]
    with open(db_filepath, "w+") as db_file:
        json.dump(db, db_file, indent=4)
    sys.exit(0)

def set_n(payload: str):
    if payload[:2] != "n=" or len(payload) < 3:
        print_save(f"{payload} is not a valid `set` payload")
        return
    payload = payload[2:]
    if not payload.isdigit():
        print_save(f"{payload} is not a valid Z set")
        return
    global n
    n = int(payload) # pylint: disable=unused-variable
    db["n"] = int(payload)
    print_save('OK')

def reduce_expr(payload: str):
    try:
        if "=" in payload:
            print_save(ZnEquation(n, payload))
        else:
            print_save(ZnExpression(n, payload))
    except (ParseError, ResolveError) as e:
        print_save("err:", e)

def solve_eq(payload: str):
    try:
        equation = ZnEquation(n, payload)
        target = equation.target_var
        solutions = equation.solve()
        print_save(target, "\u2208", set(solutions) if solutions else "{}" )
    except (ParseError, ResolveError) as e:
        print_save("err:", e)

instructions = {
    "set": set_n,
    "reduce": reduce_expr,
    "solve": solve_eq,
}

def main():
    global db_filepath
    db_filepath = Path('znop_db.json')
    if not db_filepath.is_file():
        with open(db_filepath, "w+") as db_file:
            json.dump({"n": 10, "history": []}, db_file, indent=4)

    global db
    db = json.load(open(db_filepath))

    global n
    n = db["n"]

    for line in db["history"]:
        print(line)

    while True:
        input_vals = input_save(f"\n(n={n}) ").split()
        if len(input_vals) == 1:
            if input_vals[0] == "help":
                print_save(help_info)
                continue
            elif input_vals[0] == "quit":
                quit_app()
            print_save("Invalid command, input 'help' for help")
            continue
        if len(input_vals) != 2:
            print_save("Invalid command, input 'help' for help")
            continue
        instruct, payload = input_vals
        try:
            instructions[instruct](payload)
        except KeyError:
            print_save("Invalid command, input 'help' for help")
        except Exception as e:
            print_save("Unknown err:", e)
