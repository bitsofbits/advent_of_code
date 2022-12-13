import sys

from implementation import find_decoder_key, load_packets_pairs

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    pairs = load_packets_pairs(path)
    n_packets_in_order = sum((a < b) * (i + 1) for (i, (a, b)) in enumerate(pairs))
    print("Part 1: Number of packets in order:", n_packets_in_order)
    print("Part 2: Decoder key:", find_decoder_key(pairs))
