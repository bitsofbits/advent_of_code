import random
from collections import defaultdict
from copy import deepcopy
from functools import cache
from heapq import heappop, heappush
from itertools import permutations
from math import factorial, inf, log


def parse(text):
    """
    >>> nodes, edges = parse(EXAMPLE_TEXT)
    """
    nodes = []
    edges = []
    lines = text.strip().split('\n')
    lines.sort(key=len)
    for line in lines:
        left, right = line.strip().split(':')
        left = left.strip()
        nodes.append(left)
        for right in right.strip().split():
            nodes.append(right)
            edges.append(frozenset([left, right]))
    return list(set(nodes)), edges


# Def fill dictionary of what subgraphs can be filled with
# from a location given guts


def traverse_1(nodes, outputs, start, cuts=()):
    queue = [(start, None)]
    seen = set()
    used = set()
    while queue:
        node, edge = queue.pop()
        if node in seen:
            continue
        seen.add(node)
        used.add(edge)
        for next_node in outputs[node]:
            edge = frozenset((node, next_node))
            if edge not in cuts:
                queue.append((next_node, edge))
    return len(seen), {x for x in used if x is not None}


def make_outputs(edges):
    outputs = {}
    for a, b in edges:
        if a not in outputs:
            outputs[a] = set()
        outputs[a].add(b)
        if b not in outputs:
            outputs[b] = set()
        outputs[b].add(a)
    return outputs


def count_diconnected_1(nodes, edges):
    outputs = make_outputs(edges)
    cutsets = []
    for i, e1 in enumerate(edges):
        print(i, "of", len(edges))
        for j, e2 in enumerate(edges[i + 1 :]):
            for k, e3 in enumerate(edges[i + j + 2 :]):
                for cset in cutsets:
                    if not {e1, e2, e3} & cset:
                        break
                else:
                    n, cset = traverse_1(nodes, outputs, nodes[0], cuts=(e1, e2, e3))
                    if n != len(nodes):
                        return n
                    else:
                        cutsets.append(cset)


def find_subgraphs(nodes, edges, cuts=()):
    subgraph_map = {}
    for node in nodes:
        subgraph_map[node] = frozenset([node])

    for edge in edges:
        if edge in cuts:
            continue
        nd_1, nd_2 = edge
        new_subgraph = subgraph_map[nd_1] | subgraph_map[nd_2]
        for nd in new_subgraph:
            subgraph_map[nd] = new_subgraph
    return frozenset(subgraph_map.values())


@cache
def find_subgraphs_2(nodes, edges):
    subgraph_map = {}
    for node in nodes:
        subgraph_map[node] = frozenset([node])
    for edge in edges:
        nd_1, nd_2 = edge
        new_subgraph = subgraph_map[nd_1] | subgraph_map[nd_2]
        for nd in new_subgraph:
            subgraph_map[nd] = new_subgraph
    return frozenset(subgraph_map.values())


def count_diconnected_2(nodes, edges):
    edges_set = frozenset(edges)
    nodes = frozenset(nodes)

    base_sets = frozenset((node, frozenset([node])) for node in nodes)

    @cache
    def add_edge(connected, edge):
        connected = dict(connected)
        nd_1, nd_2 = edge
        new_subgraph = connected[nd_1] | connected[nd_2]
        for nd in new_subgraph:
            connected[nd] = new_subgraph
        return frozenset(connected.items())

    def find_subgraphs_2(edges, connected):
        for edge in edges:
            connected = add_edge(connected, edge)
        return frozenset(dict(connected).values())

    # def find_subgraphs_2(nodes, edges, connected):
    #     for edge in edges:
    #         nd_1, nd_2 = edge
    #         new_subgraph = connected[nd_1] | connected[nd_2]
    #         for nd in new_subgraph:
    #             connected[nd] = new_subgraph
    #     return frozenset(connected.values())

    for i, e1 in enumerate(edges):
        print(">>>", i)
        for j, e2 in enumerate(edges[i + 1 :]):
            for k, e3 in enumerate(edges[i + j + 2 :]):
                subgraphs = find_subgraphs_2(edges_set - {e1, e2, e3}, base_sets.copy())
                if len(subgraphs) > 1:
                    [a, b] = subgraphs
                    return len(a)
    raise ValueError("found no cuts that work")


def count_diconnected_3(nodes, edges):
    edge_set = frozenset(edges)
    nodes = frozenset(nodes)

    base_sets = frozenset((node, frozenset([node])) for node in nodes)

    @cache
    def add_edge(connected, edge):
        connected = dict(connected)
        nd_1, nd_2 = edge
        new_subgraph = connected[nd_1] | connected[nd_2]
        for nd in new_subgraph:
            connected[nd] = new_subgraph
        return frozenset(connected.items()), set(connected.values())

    def traverse_edges(outputs, start, cuts=()):
        queue = [(start, None)]
        seen = set()
        used_edges = set()
        while queue:
            node, edge = queue.pop()
            if node in seen:
                continue
            seen.add(node)
            used_edges.add(edge)
            for next_node in outputs[node]:
                edge = frozenset((node, next_node))
                if edge not in cuts:
                    queue.append((next_node, edge))
        return len(seen), {x for x in used_edges if x is not None}

    # @cache
    # def find_all_subgraph_sets(edges):
    #     if len(edges) <= 3:
    #         return {base_sets}
    #     sets = set()
    #     for edge in edges:
    #         new_edges = edges - {edge}
    #         for new_connected in find_all_subgraph_sets(new_edges):
    #             sets.add(add_edge(new_connected, edge))
    #     return sets

    # for connected in find_all_subgraph_sets(edges):
    #     if len(connected) > 1:
    #         [a, b] = connected
    #         return len(a)

    # @cache
    def find_subgraphs_3(edges, connected, cuts=()):
        outputs = make_outputs(edges)
        count, used_edges = traverse_edges(outputs, list(nodes)[0], cuts=cuts)
        unused = set(edges) - used_edges
        return count, unused
        # leftover_edges = set(edges)
        # for edge in edges:
        #     connected, subsets = add_edge(connected, edge)
        #     leftover_edges.remove(edge)
        #     if len(subsets) == 1:
        #         break
        # return frozenset(dict(connected).values()), leftover_edges

    added = set()

    def add_triples(triples, leftover_edges):
        key = frozenset(leftover_edges)
        if key in added:
            return
        added.add(key)
        leftover_edges = list(leftover_edges)
        for i, e1 in enumerate(leftover_edges):
            for j, e2 in enumerate(leftover_edges[i + 1 :]):
                for e3 in enumerate(leftover_edges[i + j + 2 :]):
                    triples.add(frozenset([e1, e2, e3]))
        return triples

    # # print("warmup")
    # # _, leftover = find_subgraphs_3(edge_set, base_sets)
    # # skipable = set()
    # for i, e1 in enumerate(edges):
    #     # print("finding outer level subgraphs")
    #     # _, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1})
    #     # print("building")
    #     # skipable |= as_triples(leftover | e1)
    #     print("+++", i, "of", len(edges))
    #     for j, e2 in enumerate(edges[i + 1 :]):
    #         print("---", i, j)
    #         # _, leftover_edges_2 = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2})
    #         # leftover_edges_3 = set()
    #         for e3 in edges[i + j + 2 :]:
    #             # if frozenset({e1, e2, e3}) in skipable:
    #             #     continue
    #             n, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2, e3})
    #             # add_triples(skipable, leftover | {e1, e2, e3})
    #             if n < len(nodes):
    #                 return n

    # print("warmup")
    # _, leftover = find_subgraphs_3(edge_set, base_sets)
    # skipable = set()
    e1 = frozenset(('nct', 'kdk'))
    e2 = frozenset(('mqq', 'hpx'))
    assert e1 in edges
    # assert e2 in edges
    for e2 in edges:
        for e3 in edges:
            # print(e3)
            # break
            n, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2, e3})
            # add_triples(skipable, leftover | {e1, e2, e3})
            if n < len(nodes):
                return n

    raise ValueError("found no cuts that work")


def traverse_states(nodes, edges):
    domains = frozenset([frozenset([x]) for x in nodes])
    queue = [(domains, frozenset(edges))]
    seen_states = set()
    while queue:
        domains, remaining_edges = heappop(queue)
        if remaining_edges in seen_states:
            continue
        seen_states.add(remaining_edges)
        if len(domains) == 1:
            continue
        if len(remaining_edges) <= 3:
            if len(domains) > 1:
                return max(len(x) for x in domains)
            continue
        for next_edge in remaining_edges:
            nd1, nd2 = next_edge
            updated_domains = set()
            domain_map = {}
            for domain in domains:
                for node in domain:
                    domain_map[node] = domain
            old_domains = {domain_map[nd1], domain_map[nd2]}
            new_domain = domain_map[nd1] | domain_map[nd2]
            updated_domains = set([new_domain])
            for domain in domains:
                if domain not in old_domains:
                    updated_domains.add(domain)

            heappush(queue, (updated_domains, remaining_edges - {next_edge}))
    return len(nodes)


def count_diconnected_4(nodes, edges):
    outputs = make_outputs(edges)

    def edge_key(x):
        a, b = x
        return len(outputs[a]) * len(outputs[b])

    edges = sorted(edges, key=edge_key, reverse=True)

    edge_set = frozenset(edges)
    nodes = frozenset(nodes)

    base_sets = frozenset((node, frozenset([node])) for node in nodes)

    @cache
    def add_edge(connected, edge):
        connected = dict(connected)
        nd_1, nd_2 = edge
        new_subgraph = connected[nd_1] | connected[nd_2]
        for nd in new_subgraph:
            connected[nd] = new_subgraph
        return frozenset(connected.items()), set(connected.values())

    def traverse_edges(outputs, start, cuts=()):
        queue = [(start, None)]
        seen = set()
        # used_edges = set()
        while queue:
            node, edge = queue.pop()
            if node in seen:
                continue
            seen.add(node)
            # used_edges.add(edge)
            for next_node in outputs[node]:
                edge = frozenset((node, next_node))
                if edge not in cuts:
                    queue.append((next_node, edge))
        return len(seen)  # , {x for x in used_edges if x is not None}

    # @cache
    # def find_all_subgraph_sets(edges):
    #     if len(edges) <= 3:
    #         return {base_sets}
    #     sets = set()
    #     for edge in edges:
    #         new_edges = edges - {edge}
    #         for new_connected in find_all_subgraph_sets(new_edges):
    #             sets.add(add_edge(new_connected, edge))
    #     return sets

    # for connected in find_all_subgraph_sets(edges):
    #     if len(connected) > 1:
    #         [a, b] = connected
    #         return len(a)

    # @cache
    def find_subgraphs_3(edges, connected, cuts=()):
        outputs = make_outputs(edges)
        count, used_edges = traverse_edges(outputs, list(nodes)[0], cuts=cuts)
        unused = set(edges) - used_edges
        return count, unused
        # leftover_edges = set(edges)
        # for edge in edges:
        #     connected, subsets = add_edge(connected, edge)
        #     leftover_edges.remove(edge)
        #     if len(subsets) == 1:
        #         break
        # return frozenset(dict(connected).values()), leftover_edges

    added = set()

    def add_triples(triples, leftover_edges):
        key = frozenset(leftover_edges)
        if key in added:
            return
        added.add(key)
        leftover_edges = list(leftover_edges)
        for i, e1 in enumerate(leftover_edges):
            for j, e2 in enumerate(leftover_edges[i + 1 :]):
                for e3 in enumerate(leftover_edges[i + j + 2 :]):
                    triples.add(frozenset([e1, e2, e3]))
        return triples

    print("warmup")
    # _, leftover = find_subgraphs_3(edge_set, base_sets)
    # skipable = set()
    for i, e1 in enumerate(edges):
        # print("finding outer level subgraphs")
        # _, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1})
        # print("building")
        # skipable |= as_triples(leftover | e1)
        print("+++)", i, "of", len(edges))
        for j, e2 in enumerate(edges[i + 1 :]):
            print("---", i, j)
            # _, leftover_edges_2 = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2})
            # leftover_edges_3 = set()
            for e3 in edges[i + j + 2 :]:
                # if frozenset({e1, e2, e3}) in skipable:
                #     continue
                n, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2, e3})
                # add_triples(skipable, leftover | {e1, e2, e3})
                if n < len(nodes):
                    return n
    raise ValueError("found no cuts that work")


# _edge_name_counter = 0


# def get_new_node():
#     global _edge_name_counter
#     _edge_name_counter += 1
#     return f"NEW_NODE_{_edge_name_counter}"


def karger_contract(nodes_to_edges, edges, final_vertext_count=2):
    # Karger: https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Could also use Stoer–Wagner

    nodes_to_edges = deepcopy(nodes_to_edges)
    edges = edges.copy()

    while len(nodes_to_edges) > final_vertext_count:
        [target_edge] = random.choices(tuple(edges.keys()), tuple(edges.values()))
        node_1, node_2 = target_edge
        new_node = node_1 | node_2
        assert new_node not in nodes_to_edges
        edges_to_add = defaultdict(int)
        edges_to_remove = set()

        for edge_node in target_edge:
            assert edge_node in nodes_to_edges
            for obsolete_edge in nodes_to_edges[edge_node]:
                node_a, node_b = obsolete_edge
                if obsolete_edge == target_edge:
                    edges_to_remove.add(obsolete_edge)
                elif node_a in target_edge:
                    assert node_b not in target_edge
                    new_edge = frozenset([node_b, new_node])
                    edges_to_add[new_edge] += edges[obsolete_edge]
                    edges_to_remove.add(obsolete_edge)
                elif node_b in target_edge:
                    assert node_a not in target_edge
                    new_edge = frozenset([node_a, new_node])
                    edges_to_add[new_edge] += edges[obsolete_edge]
                    edges_to_remove.add(obsolete_edge)
                else:
                    raise ValueError(obsolete_edge)

        for e, n in edges_to_add.items():
            assert e not in edges
            edges[e] = n
            for nd in e:
                if nd in nodes_to_edges:
                    nodes_to_edges[nd].add(e)
                else:
                    nodes_to_edges[nd] = {e}

        for e in edges_to_remove:
            del edges[e]
            for nd in e:
                nodes_to_edges[nd].remove(e)

        nodes_to_remove = [k for (k, v) in nodes_to_edges.items() if not v]
        for k in nodes_to_remove:
            nodes_to_edges.pop(k)

    return nodes_to_edges, edges


def count_edges(edges):
    return sum(edges.values())


def karger_stein_contract(nodes_to_edges, edges):
    if len(nodes_to_edges) < 6:
        return karger_contract(nodes_to_edges, edges)
    t = 1 + len(nodes_to_edges) / 2**0.5
    G1 = karger_contract(nodes_to_edges, edges, t)
    G2 = karger_contract(nodes_to_edges, edges, t)
    return min(
        karger_stein_contract(*G1),
        karger_stein_contract(*G2),
        key=lambda x: count_edges(x[1]),
    )


@cache
def mangle_edges(edges):
    return {frozenset([frozenset([a]), frozenset([b])]): 1 for (a, b) in edges}


@cache
def make_nodes_to_edges(edges):
    mangled_edges = {frozenset([frozenset([a]), frozenset([b])]): 1 for (a, b) in edges}

    nodes_to_edges = defaultdict(set)
    for edge in mangled_edges:
        a, b = edge
        nodes_to_edges[a].add(edge)
        nodes_to_edges[b].add(edge)
    return dict(nodes_to_edges)


def find_min_cuts(edges, n=3):
    mangled_edges = mangle_edges(edges)
    nodes_to_edges = make_nodes_to_edges(edges)

    # This gives reasonable success probability for Karger-Stein
    iterations = int(round(log(len(nodes_to_edges))))

    best_count = inf
    for _ in range(iterations):
        nodes_to_edges, candidate_edges = karger_stein_contract(
            nodes_to_edges, mangled_edges
        )
        count = count_edges(candidate_edges)
        if count < best_count:
            best_count = count
            [(a_nodes, b_nodes)] = candidate_edges

    choices = (frozenset((a, b)) for a in a_nodes for b in b_nodes)
    choices = (x for x in choices if x in edges)
    return permutations(choices, n)


def count_diconnected_5(nodes, edges):
    start = nodes[0]
    nodes = frozenset(nodes)

    def traverse(nodes, outputs, start, cuts=()):
        queue = [(start, None)]
        seen = set()
        while queue:
            node, edge = queue.pop()
            if node in seen:
                continue
            seen.add(node)
            for next_node in outputs[node]:
                edge = frozenset((node, next_node))
                if edge not in cuts:
                    queue.append((next_node, edge))
        return len(seen)

    outputs = make_outputs(edges)
    edges = tuple(edges)
    tried = set()
    while True:
        for cuts in find_min_cuts(edges):
            if cuts in tried:
                continue
            # print("Trying", cuts)
            n = traverse(nodes, outputs, start, cuts=cuts)
            if n < len(nodes):
                return n


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    54

    inputs -> 532891
    """
    nodes, edges = parse(text)
    # n = count_diconnected_3(nodes, edges)

    n = count_diconnected_5(nodes, edges)

    return n * (len(nodes) - n)
    # nodes, edges = parse(text)
    # # outputs = make_outputs(edges)
    # n = traverse_states(nodes, edges)
    # return n * (len(nodes) - n)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    lines = INPUT_TEXT.strip().split('\n')
    new_lines = []
    for line in lines:
        line = line.replace(':', ' -- {') + ' }'
        new_lines.append(line)
    text = '\n'.join(new_lines)
    with open(data_dir / "graph.dot", 'w') as f:
        f.write(text)

    doctest.testmod()
