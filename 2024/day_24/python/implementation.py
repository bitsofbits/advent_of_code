from itertools import combinations, product
from typing import NamedTuple, Literal, Any
from functools import cache

def parse(text):
    """
    >>> vals, gates = parse(EXAMPLE_TEXT)
    >>> vals
    {'x00': 1, 'x01': 1, 'x02': 1, 'y00': 0, 'y01': 1, 'y02': 0}
    >>> gates
    {'z00': ('x00', 'AND', 'y00'), 'z01': ('x01', 'XOR', 'y01'), 'z02': ('x02', 'OR', 'y02')}
    """
    val_text, gate_text = text.strip().split('\n\n')
    values = {}
    for row in val_text.strip().split('\n'):
        key, val = row.split(': ')
        values[key] = int(val)
    gates = {}
    for row in gate_text.strip().split('\n'):
        k1, op, k2, _, key = row.strip().split()
        gates[key] = (k1, op, k2)

    return values, gates



class Value(NamedTuple):
    """
    >>> Value(name='x3').evaluate((1, 0, 1, 1), (0, 1, 0, 1))
    1
    """
    name : str

    @cache
    def evaluate(self, x, y):
        i = int(self.name[1:])
        match self.name[0]:
            case 'x':
                return x[i]
            case 'y':
                return y[i]
            case _:
                raise ValueError(self.name)

class Operation(NamedTuple):
    """
    >>> a = Value('x3')
    >>> b = Value('y3')
    >>> op = Operation(a, b, 'XOR')
    >>> op.evaluate((1, 0, 1, 1), (0, 1, 0, 1))
    0
    """
    a : Any
    b : Any
    op : Literal['AND', 'OR', 'XOR']

    @cache
    def evaluate(self, x, y):
        a = self.a.evaluate(x, y)
        b = self.b.evaluate(x, y)
        match self.op:
            case 'AND':
                return a & b
            case 'OR':
                return a | b
            case 'XOR':
                return a ^ b
            case _:
                raise ValueError(self.op)

def build_op_values(gates):
    values = {}
    for k1, _, k2 in gates.values():
        for key in [k1, k2]:
            if key[0] in 'xy':
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
                processed_gates[key] = Operation(a, b, op)
                pending_deletions.add(key)
        for key in pending_deletions:
           unprocessed_gates.pop(key)
    return processed_gates


def build_values(values):
    max_xi = max_yi = 0
    for key in values:
        i = int(key[1:])
        if key[0] == 'x':
            max_xi = max(max_xi, i)
        elif key[0] == 'y':
            max_yi = max(max_yi, i)
        else:
            raise ValueError(key)
    x_values = [None] * (max_xi + 1)
    y_values = [None] * (max_yi + 1)
    for key, v in values.items():
        i = int(key[1:])
        if key[0] == 'x':
            x_values[i] = v
        elif key[0] == 'y':
            y_values[i] = v
        else:
            raise ValueError(key)
    return tuple(x_values), tuple(y_values)  



def compute(gate, values):
    k1, op, k2 = gate
    if op == 'AND':
        return values[k1] & values[k2]
    elif op == 'OR':
        return values[k1] | values[k2]
    elif op == 'XOR':
        return values[k1] ^ values[k2]
    else:
        raise ValueError(op)




def compute_dependencies_of(key, gates):
    pending = [key]
    dependencies = set()
    while pending:
        k = pending.pop()
        if k in dependencies:
            continue
        dependencies.add(k)
        if k[0] in 'xy':
            continue
        a, _, b = gates[k]
        pending.append(a)
        pending.append(b)
    return dependencies


def compute_raw_output(values, gates):
    values = values.copy()
    gates = gates.copy()
    while gates:
        completed = set()
        for key, gate in gates.items():
            try:
                values[key] = compute(gate, values)
            except KeyError as err:
                if key.startswith('x') or key.startswith('y'):
                    print(err)
                pass
            else:
                completed.add(key)
        for k in completed:
            gates.pop(k)
    return {k : v for (k, v) in values.items() if k.startswith('z')}


def compute_output(operations, values):
    output = 0
    for k in reversed(sorted(operations)):
        if k.startswith('z'):
            output = (output << 1) + operations[k].evaluate(*values)
    return output

    # values = compute_raw_output(values, gates)

    # output = 0
    # for k in reversed(sorted(values)):
    #     if k.startswith('z'):
    #         output = (output << 1) + values[k]
    # return output    

def part_1(text):
    """
    >>> part_1(EXAMPLE2_TEXT)
    2024
    """
    raw_values, gates = parse(text)
    operations = build_operations(gates)
    values = build_values(raw_values)


    return compute_output(operations, values)



def bad_bits(gates, bits):
    values = {}
    for i in range(bits):
        values[f'x{i:02d}'] = values[f'y{i:02d}'] = False

    for i in range(bits - 1):
        test_values = values.copy()
        for x in [False, True]:
            for y in [False, True]:
                test_values[f'x{i:02d}'] = x
                test_values[f'y{i:02d}'] = y
                outputs = compute_raw_output(test_values, gates)
                if outputs[f'z{i:02d}'] != x ^ y:
                    yield f'z{i:02d}'
                if outputs[f'z{i + 1:02d}'] != x & y:
                    yield f'z{i:02d}'


def is_valid(gates, bits, keys=None):
    for x in bad_bits(gates, bits):
        if keys is None or x in keys:
            return False
    return True


def is_valid_and(gates, bits, keys=None):
    values = {}
    for i in range(bits):
        values[f'x{i:02d}'] = values[f'y{i:02d}'] = False

    for i in range(bits):
        test_values = values.copy()
        key_z = f'z{i:02d}'
        if key_z not in keys:
            continue
        for x in [False, True]:
            for y in [False, True]:
                test_values[f'x{i:02d}'] = x
                test_values[f'y{i:02d}'] = y
                outputs = compute_raw_output(test_values, gates)
                if outputs[key_z] != x & y:
                    return False
    return True


def part_2(text, swaps=4, validation=is_valid):
    """
    >>> part_2(EXAMPLE3_TEXT, swaps=2, validation=is_valid_and)
    """
    # values, gates = parse(text)
    # bits = sum(1 for x in gates if x.startswith('z'))

    # bad_output_bits = set((bad_bits(gates, bits)))

    # # potentially_useful_gates = set()
    # # for i in range(bits):
    # #     if i not in bad_output_bits:
    # #         key = f'z{i:02d}'
    # #         raw_candidates = compute_dependencies_of(key, gates)
    # #         potentially_useful_gates |= raw_candidates

    # candidates = {}
    # for key in sorted(bad_output_bits):
    #     raw_candidates = compute_dependencies_of(key, gates)
    #     # raw_candidates = {x for x in raw_candidates if x not in useful_gates}
    #     raw_candidates = {x for x in raw_candidates if x[0] not in 'xy'}
    #     candidates[key] = raw_candidates

    # # for key in candidates:
    # #     print(key, ">>>", candidates[key])

    # # print(len(candidates))

    # swaps = set()
    # for key_a in candidates:
    #     print(key_a)
    #     for key_b in candidates:
    #         # It looks like we are probably swapping between groups
    #         pairs = set(product(candidates[key_a], candidates[key_b]))
    #         print(len(pairs))
    #         for pair in pairs:
    #             if pair in swaps:
    #                 continue
    #             k1, k2 = pair
    #             if k1 == k2:
    #                 continue
    #             swapped_gates = gates.copy()
    #             swapped_gates[k1], swapped_gates[k2] = swapped_gates[k2], swapped_gates[k1]
    #             if validation(swapped_gates, bits, keys=(key_a, key_b)):
    #                 swaps.add(frozenset(pair))

    # print(swaps)

    # # pairs = list(combinations(gates, 2))
    # print(len(pairs))
    # print(len(list(combinations(pairs, swaps))))
    # for groups in combinations(combinations(gates, 2), swaps):
    #     swapped_gates = gates.copy()
    #     for k1, k2 in groups:
    #         swapped_gates[k1], swapped_gates[k2] = swapped_gates[k2], swapped_gates[k1]
    #     # adjust gates
    #     if validation(swapped_gates, bits):
    #         names = set()
    #         for x in groups:
    #             names |= set(x)
    #         return ','.join(sorted(names))




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
    doctest.testmod()
