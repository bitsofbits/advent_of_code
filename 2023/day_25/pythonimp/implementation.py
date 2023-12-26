import random
from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from math import inf


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

    print("warmup")
    # _, leftover = find_subgraphs_3(edge_set, base_sets)
    skipable = set()
    for i, e1 in enumerate(edges):
        # print("finding outer level subgraphs")
        # _, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1})
        # print("building")
        # skipable |= as_triples(leftover | e1)
        print("+++", i, "of", len(edges))
        for j, e2 in enumerate(edges[i + 1 :]):
            print("---", i, j)
            # _, leftover_edges_2 = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2})
            # leftover_edges_3 = set()
            for e3 in edges[i + j + 2 :]:
                if frozenset({e1, e2, e3}) in skipable:
                    continue
                n, leftover = find_subgraphs_3(edge_set, base_sets, cuts={e1, e2, e3})
                add_triples(skipable, leftover | {e1, e2, e3})
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


def _contract(edges, n=1):
    # Karger: https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Could also use Stoer–Wagner

    unique_edges = set(edges)

    while len(unique_edges) > n:
        edge_to_remove = random.choice(list(edges))
        node_1, node_2 = edge_to_remove
        new_node = node_1 | node_2
        new_edges = []
        doomed_edges = set()
        for edge in edges:
            if edge == edge_to_remove:
                doomed_edges.add(edge)
                continue
            node_a, node_b = edge
            if node_a in (node_1, node_2):
                assert node_b not in (node_1, node_2)
                new_edges.append(frozenset([node_b, new_node]))
                doomed_edges.add(edge)
            if node_b in (node_1, node_2):
                assert node_a not in (node_1, node_2)
                new_edges.append(frozenset((node_a, new_node)))
                doomed_edges.add(edge)
        edges = [x for x in edges if x not in doomed_edges]
        edges += new_edges
        unique_edges -= doomed_edges
        unique_edges |= set(new_edges)
    return edges


def _fast_contract(edges):
    # print(len(nodes))
    n_edges = len(set(edges))
    if n_edges < 6:
        return _contract(edges)
    t = int(round(1 + n_edges / 2**0.5))
    G1 = _contract(edges, t)
    G2 = _contract(edges, t)
    # print(t, len(G1[0]), len(set(G1[1])))
    # print(t, len(G1[0]), len(set(G1[1])))
    e1 = _fast_contract(G1)
    e2 = _fast_contract(G2)
    if len(set(e1)) < len(set(e2)):
        return e1
    else:
        return e2


def contract(nodes, edges):
    count = inf
    # nodes = set([frozenset([x]) for x in nodes])
    mangled_edges = list(
        frozenset([frozenset([a]), frozenset([b])]) for (a, b) in edges
    )

    for _ in range(len(nodes)):
        candidate_edges = _fast_contract(mangled_edges)
        if len(candidate_edges) < count:
            [edge] = set(candidate_edges)
            count = len(candidate_edges)
    a, b = (list(x) for x in edge)
    choices = []
    for nd1 in a:
        for nd2 in b:
            edge = frozenset([nd1, nd2])
            if edge in edges:
                choices.append(edge)
    for i, a in enumerate(choices):
        for j, b in enumerate(choices[i + 1 :]):
            for c in choices[i + j + 2 :]:
                yield (a, b, c)


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

    tried = set()
    for i in range(10000):
        for cuts in contract(nodes, edges):
            if cuts in tried:
                continue
            n = traverse(nodes, outputs, start, cuts=cuts)
            if n < len(nodes):
                return n

    raise ValueError("found no cuts that work")


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    54
    """
    nodes, edges = parse(text)
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

    doctest.testmod()
