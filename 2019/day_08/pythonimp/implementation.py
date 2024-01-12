def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    """
    return [int(x) for x in text.strip()]


def make_layers(values, width, height):
    layers = []
    n_layers = len(values) // (width * height)
    assert len(values) % n_layers == 0
    for i in range(n_layers):
        layer = []
        layers.append(layer)
        for j in range(height):
            row = []
            layer.append(row)
            for k in range(width):
                row.append(values[i * width * height + j * width + k])
    return layers


def count_digits(layer, value):
    n = 0
    for row in layer:
        for x in row:
            if x == value:
                n += 1
    return n


def part_1(text, width=25, height=6):
    """
    >>> part_1(EXAMPLE_TEXT, 3, 2)
    1

    196 is too low
    """
    values = parse(text)
    layers = make_layers(values, width, height)
    min_zero_layer = None
    min_zeros = width * height + 1
    for layer in layers:
        n_zeros = count_digits(layer, 0)
        if n_zeros < min_zeros:
            min_zero_layer = layer
            min_zeros = n_zeros
    return count_digits(min_zero_layer, 1) * count_digits(min_zero_layer, 2)


def decode(layers, width, height):
    decoded = layers[-1]
    for i in reversed(range(len(layers) - 1)):
        for j in range(height):
            for k in range(width):
                top_pixel = layers[i][j][k]
                if top_pixel != 2:
                    decoded[j][k] = top_pixel
    return decoded


def render(image):
    scan_lines = []
    for row in image:
        scan_lines.append(''.join('# X'[x] for x in row))
    return '\n'.join(scan_lines)


def part_2(text, width=25, height=6):
    """
    >>> part_2("0222112222120000", 2, 2)

    JAFRA?
    """
    values = parse(text)
    layers = make_layers(values, width, height)
    decoded = decode(layers, width, height)
    print(render(decoded))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    doctest.testmod()
