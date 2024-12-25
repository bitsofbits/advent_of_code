from itertools import combinations,  product
from typing import Literal, Any
from dataclasses import dataclass

def parse(text):
    """
    >>> vals, gates = parse(EXAMPLE_TEXT)
    >>> vals
    {'x00': 1, 'x01': 1, 'x02': 1, 'y00': 0, 'y01': 1, 'y02': 0}
    >>> gates
    {'z00': ('x00', 'AND', 'y00'), 'z01': ('x01', 'XOR', 'y01'), 'z02': ('x02', 'OR', 'y02')}
    """
    val_text, gate_text = text.strip().split("\n\n")
    values = {}
    for row in val_text.strip().split("\n"):
        key, val = row.split(": ")
        values[key] = int(val)
    gates = {}
    for row in gate_text.strip().split("\n"):
        k1, op, k2, _, key = row.strip().split()
        gates[key] = (k1, op, k2)

    return values, gates


@dataclass
class Value:
    """
    >>> Value(name='x3').evaluate(values={'x3' : 1})
    1
    """

    name: str

    def evaluate(self, values, skip_overrides=False):
        x = values[self.name]
        if isinstance(x, (Operation, Value)):
            return x.evaluate(values)
        else:
            return x
        


@dataclass
class Operation:
    """
    >>> a = Value('x3')
    >>> b = Value('y3')
    >>> op = Operation('op1', a, b, 'XOR')
    >>> op.evaluate(values={'x3': 1, 'y3' : 1})
    0

    # >>> c = Value('y0')
    # >>> op.evaluate((1, 0, 1, 1), (0, 1, 0, 1), swaps=frozenset([('y3', c)]))
    # 1
    """

    name: str
    a: Any
    b: Any
    op: Literal["AND", "OR", "XOR"]

    def evaluate(self, values=None, skip_overrides=False):
        x = values.get(self.name)
        if x is not None and not skip_overrides:
            if isinstance(x, (Operation, Value)):
                return x.evaluate(values, skip_overrides=True)
            else:
                return x
        a = self.a.evaluate(values)
        b = self.b.evaluate(values)
        match self.op:
            case "AND":
                return a & b
            case "OR":
                return a | b
            case "XOR":
                return a ^ b
            case _:
                raise ValueError(self.op)




def build_op_values(gates):
    values = {}
    for k1, _, k2 in gates.values():
        for key in [k1, k2]:
            if key[0] in "xy":
                values[key] = Value(key)
    return values


def build_operations(gates):
    # gates = dict[output] -> (k1, op, k2)
    unprocessed_gates = gates.copy()
    processed_gates = build_op_values(gates)
    while unprocessed_gates:
        pending_deletions = set()
        for key in unprocessed_gates:
            a, op, b = gates[key]
            if a in processed_gates and b in processed_gates:
                a = processed_gates[a]
                b = processed_gates[b]
                processed_gates[key] = Operation(key, a, b, op)
                pending_deletions.add(key)
        for key in pending_deletions:
            unprocessed_gates.pop(key)
    return processed_gates


# def build_values_map(values):
#     map_ = {}
#     for key, v in values.items():
#         i = int(key[1:])
#         if key[0] == 'x':
#             map
#         elif key[0] == 'y':
#             y_values[i] = v
#         else:
#             raise ValueError(key)
#     return tuple(x_values), tuple(y_values)


def compute_output(operations, values):
    output = 0
    for k in reversed(sorted(operations)):
        if k.startswith("z"):
            output = (output << 1) + operations[k].evaluate(values)
    return output


def part_1(text):
    """
    >>> part_1(EXAMPLE2_TEXT)
    2024
    """
    values, gates = parse(text)
    operations = build_operations(gates)
    return compute_output(operations, values)


def build_half_adder(i, x=None, y=None, prefix=""):
    if x is None:
        x = Value(name=f"x{i:02d}")
    if y is None:
        y = Value(name=f"y{i:02d}")
    sum_ = Operation(prefix + f"sum_{i}", x, y, "XOR")
    carry = Operation(prefix + f"carry{i}", x, y, "AND")
    return sum_, carry


def build_adder(i, carry):
    half_sum, half_carry = build_half_adder(i, prefix="half_")
    sum_ = Operation(f"sum_{i}", half_sum, carry, "XOR")
    carry = Operation(
        f"carry_{i}", half_carry, Operation(f"merge_{i}", carry, half_sum, "AND"), "OR"
    )
    return sum_, carry


def equivalent_over(keys, op1, op2):
    # TODO: also check size?
    series = [[(k, 0), (k, 1)] for k in keys]
    for items in product(*series):
        values = dict(items)
        try:
            if op1.evaluate(values) != op2.evaluate(values):
                return False
        except KeyError:
            return False
    return True
    
def extract_ops_down_to(terminal_keys, op):
    pending = [op]
    ops = []
    while pending:
        op = pending.pop()
        if op in ops or op.name in terminal_keys:
            continue
        ops.append(op)
        if isinstance(op, Operation):
            pending.append(op.a)
            pending.append(op.b)
    return ops

def extract_keys_down_to(terminal_keys, op):
    return {x.name for x in extract_ops_down_to(terminal_keys, op)}

def find_swap_target(input_names, add, operations):     
    examples = extract_ops_down_to(input_names, add)
    for example, candidate in product(examples, operations.values()):
        if equivalent_over(input_names, example, candidate):
            return candidate


def swap_ops(op_x, op_y, operations):
    name_x = op_x.name
    name_y = op_y.name

    for k, v in operations.items():
        if isinstance(v, Operation):
            new_a = v.a
            new_b = v.b
            if v.a.name == name_x:
                new_a = op_y
            if v.b.name == name_x:
                new_b = op_y
            if v.a.name == name_y:
                new_a = op_x
            if v.b.name == name_y:
                new_b = op_x
            v.a = new_a
            v.b = new_b

    for k, v in operations.items():
        if v.name == name_x:
            v.name = name_y
        elif v.name == name_y:
            v.name = name_x

    operations[name_x], operations[name_y] = operations[name_y], operations[name_x]
    for name in [name_x, name_y]:
        assert operations[name].name == name

    for k, v in operations.items():
        assert v.name == k




def part_2(text, swaps=4):
    """
    >>> part_2(DATA_TEXT)
    """
    raw_values, gates = parse(text)
    operations = build_operations(gates)
    # x_len, y_len = (len(x) for x in build_values(raw_values))
    # assert x_len == y_len

    add_0, carry_0 = build_half_adder(0)

    for k, v in operations.items():
        if equivalent_over(['x00', 'y00'], carry_0, v):
                break
    else:
        raise ValueError('no carry_0 match')
    last_carry = Value(k)


    swapped = []
    for i in range(1, 45):
        add, carry = build_adder(i, last_carry)
        key = f'z{i:02d}'
        op = operations[key]
        input_names = [f'x{i:02d}', f'y{i:02d}', last_carry.name]

        if not equivalent_over(input_names, add, op):
            swap_target = find_swap_target(input_names, add, operations)
            for swap_source in [op, op.a, op.b]:
                swap_ops(swap_source, swap_target, operations)
                test_op = operations[key]
                if equivalent_over(input_names, add, test_op):
                    swapped.extend((swap_source.name, swap_target.name))
                    break
                swap_ops(swap_source, swap_target, operations)
            else:

                raise ValueError('no swap found for Add', i)
    

        for k, v in operations.items():
            if equivalent_over(input_names, carry, v):
                break
        else:
            print('no carry', i, 'match')

        last_carry = Value(k)

    return ','.join(sorted(swapped))

   

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "example3.txt") as f:
        EXAMPLE3_TEXT = f.read()
    with open(data_dir / "data.txt") as f:
        DATA_TEXT = f.read()
    doctest.testmod()
