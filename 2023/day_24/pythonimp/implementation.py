from math import ceil, inf


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [((19, 13, 30), (-2, 1, -2)), ((18, 19, 22), (-1, -1, -2))]
    """
    for line in text.strip().split("\n"):
        p_text, v_text = line.strip().split("@")
        p = tuple(int(x) for x in p_text.strip().split(', '))
        v = tuple(int(x) for x in v_text.strip().split(', '))
        yield p, v


def xy_intersect(points):
    """
    x = x1 + vx1 t
    y = y1 + vy1 t => t = (y - y1) / vy1
    => x = x1 + vx1 / vy1 (y - y1)
    or y = y1 + vy1 / vx1 (x - x1) = (y1 - vy1 / vx1 x1) + vy1 / vx1 x = ax + c

    """
    for i, (p1, v1) in enumerate(points):
        x1, y1, _ = p1
        vx1, vy1, _ = v1
        for p2, v2 in points[i + 1 :]:
            x2, y2, _ = p2
            vx2, vy2, _ = v2
            #
            a = vy1 / vx1
            b = vy2 / vx2
            c = y1 - a * x1
            d = y2 - b * x2

            if a - b != 0:
                x = (d - c) / (a - b)
                y = a * x + c
                t_a = (x - x1) / vx1
                t_b = (x - x2) / vx2

                yield x, y, t_a, t_b
            else:
                yield 0, 0, -inf, -inf


def part_1(text, min_xy=200000000000000, max_xy=400000000000000):
    """
    >>> part_1(EXAMPLE_TEXT, 7, 27)
    2

    inputs -> 14672
    """
    points = list(parse(text))
    count = 0
    for x, y, t_x, t_y in xy_intersect(points):
        if t_x >= 0 and t_y >= 0 and min_xy <= x <= max_xy and min_xy <= y <= max_xy:
            count += 1
    return count


def close(a, b, epsilon=1e-3):
    return abs(a - b) < epsilon


def intersecting_rock_coordinates(points, trials=100):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3




    p2 = r2 + v2 t
    p3 = ....



    """
    augmented_points = []
    for X, V in points:
        *_, z = X
        assert z > 0
        *_, vz = V
        if vz >= 0:
            t_0 = inf
        else:
            t_0 = int(ceil(-z / vz))
        augmented_points.append((t_0, X, V))
    augmented_points.sort()

    T0, R0, V0 = augmented_points[0]
    T1, R1, V1 = augmented_points[1]
    T2, R2, V2 = augmented_points[2]

    for t0 in range(T0 + 1):
        x0, y0, z0 = (r + v * t0 for (r, v) in zip(R0, V0))
        for t1 in range(T1 + 1):
            if t1 == t0:
                continue
            x1, y1, z1 = (r + v * t1 for (r, v) in zip(R1, V1))
            dt = t1 - t0
            vx = (x1 - x0) / dt
            vy = (y1 - y0) / dt
            vz = (z1 - z0) / dt
            # if abs(vx) < 0 or abs(vy) < 0 or abs(vz) < 0:
            #     break
            if not all(close(x - round(x), 0) for x in (vx, vy, vz)):
                continue
            V = (vx, vy, vz)
            R = tuple((r - v * t0 for (r, v) in zip((x0, y0, z0), V)))

            # x2 = r2_x + t2 * v2_x = Rx + vx * t2 => t2 = (r2_x - Rx) / (vx - v2_x)
            if V[0] == V2[0]:
                continue
            t2 = (R2[0] - R[0]) / (V[0] - V2[0])
            if not close(t2 - round(t2), 0):
                continue
            assert t2 <= T2
            # for t2 in range(trials):
            x2, y2, z2 = (r + v * t2 for (r, v) in zip(R2, V2))
            x, y, z = (r + v * (t2 - t1) for (r, v) in zip((x1, y1, z1), V))
            if all(close(a, b) for (a, b) in zip([x2, y2, z2], [x, y, z])):
                return R, V


def intersecting_rock_coordinates(points, trials=100):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3




    p2 = r2 + v2 t
    p3 = ....



    """
    augmented_points = []
    for X, V in points:
        *_, z = X
        assert z > 0
        *_, vz = V
        if vz >= 0:
            t_0 = inf
        else:
            t_0 = int(ceil(-z / vz))
        augmented_points.append((t_0, X, V))
    augmented_points.sort()

    T0, R0, V0 = augmented_points[0]
    T1, R1, V1 = augmented_points[1]
    T2, R2, V2 = augmented_points[2]

    forbidden_vx = {x[2][0] for x in augmented_points}
    candidate_vx = [(-1 if (i % 2) else 2) * (i // 2) for i in range(2, 2 * trials)]
    candidate_vx = [x for x in candidate_vx if x not in forbidden_vx]
    # print(len(candidate_vx), 2 * trials - 2)
    # print(forbidden_vx)

    for dt in range(1, trials):
        # print(dt)
        for t0 in range(trials):
            x0, y0, z0 = (r + v * t0 for (r, v) in zip(R0, V0))
            for t1 in [t0 - dt, t0 + dt]:
                # for vx in [-abs_vx, abs_vx]:
                # xs = x0 - vx * t0
                # if vx == V1[0]:
                #         continue
                # t1 = (xs - R1[0]) / (V1[0] - vx)
                if t1 == t0:
                    continue
                x1, y1, z1 = (r + v * t1 for (r, v) in zip(R1, V1))
                dt = t1 - t0
                vx = (x1 - x0) / dt
                vy = (y1 - y0) / dt
                vz = (z1 - z0) / dt
                # if abs(vx) < 0 or abs(vy) < 0 or abs(vz) < 0:
                #     break
                if not all(close(x - round(x), 0) for x in (vx, vy, vz)):
                    continue
                V = (vx, vy, vz)
                R = tuple((r - v * t0 for (r, v) in zip((x0, y0, z0), V)))

                # x2 = r2_x + t2 * v2_x = Rx + vx * t2 => t2 = (r2_x - Rx) / (vx - v2_x)
                if V[0] == V2[0]:
                    continue
                t2 = (R2[0] - R[0]) / (V[0] - V2[0])
                if not close(t2 - round(t2), 0):
                    continue
                assert t2 <= T2
                # for t2 in range(trials):
                x2, y2, z2 = (r + v * t2 for (r, v) in zip(R2, V2))
                x, y, z = (r + v * (t2 - t1) for (r, v) in zip((x1, y1, z1), V))
                if all(close(a, b) for (a, b) in zip([x2, y2, z2], [x, y, z])):
                    return R, V


def intersecting_rock_coordinates_2(points, trials=10):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3


    p2 = r2 + v2 t
    p3 = ....


    """

    R0, V0 = points[0]
    R1, V1 = points[1]
    R2, V2 = points[2]

    # R0, V0 is a line, in plane-0 that intersects the line
    # R1, V1 is a line, in plane-1 that intersects the line
    # Rs0 is a point on the line and on plane-0
    # Rs0, R1, V1 define a plane

    for t0 in range(1, trials):
        Rs0 = tuple(r + v * t0 for (r, v) in zip(R0, V0))
        # n1 is perpendicular to the plane defined by L1 and Rs0 -- should contain line
        n1 = cross(vsub(Rs0, R1), vsub(Rs0, vadd(R1, V1)))
        N = None
        for R, V in points[2:]:
            if N is None:
                # n1 is perpendicular to the plane defined by L2 and Rs0 -- should contain line
                n2 = cross(vsub(Rs0, R), vsub(Rs0, vadd(R, V)))
                # n is perpendicular to n0 and n1 and should be aligned with line
                n = cross(n1, n2)
                if dot(n, n) < 1e-3:
                    continue
                N = n
            # print(t0, N)
            metric = dot(cross(N, V), vsub(Rs0, R))
            if abs(metric) > 1e-3:
                N = None
                break
        if N is not None:
            break
    else:
        raise ValueError("couldn't find compatible normal")

    for t1 in range(1, trials):
        if t1 == t0:
            continue
        x0, y0, z0 = Rs0
        if t1 == t0:
            continue
        x1, y1, z1 = (r + v * t1 for (r, v) in zip(R1, V1))
        dt = t1 - t0
        vx = (x1 - x0) / dt
        vy = (y1 - y0) / dt
        vz = (z1 - z0) / dt
        # if abs(vx) < 0 or abs(vy) < 0 or abs(vz) < 0:
        #     break
        if not all(close(x - round(x), 0) for x in (vx, vy, vz)):
            continue
        V = (vx, vy, vz)
        R = tuple((r - v * t0 for (r, v) in zip((x0, y0, z0), V)))

        # x2 = r2_x + t2 * v2_x = Rx + vx * t2 => t2 = (r2_x - Rx) / (vx - v2_x)
        if V[0] == V2[0]:
            continue
        t2 = (R2[0] - R[0]) / (V[0] - V2[0])
        if not close(t2 - round(t2), 0):
            continue
        # assert t2 <= T2
        # for t2 in range(trials):
        x2, y2, z2 = (r + v * t2 for (r, v) in zip(R2, V2))
        x, y, z = (r + v * (t2 - t1) for (r, v) in zip((x1, y1, z1), V))
        if all(close(a, b) for (a, b) in zip([x2, y2, z2], [x, y, z])):
            return R, V
    raise RuntimeError("couldn't find value from normal :-(")


def intersecting_rock_coordinates_3(points, trials=10):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3


    p2 = r2 + v2 t
    p3 = ....


    """

    augmented_points = []
    for X, V in points:
        *_, z = X
        assert z > 0
        *_, vz = V
        if vz >= 0:
            t_0 = inf
        else:
            t_0 = int(ceil(-z / vz))
        augmented_points.append((t_0, X, V))
    augmented_points.sort()
    points = [x[1:] for x in augmented_points]

    R0, V0 = points[0]
    R1, V1 = points[1]
    R2, V2 = points[2]

    # R0, V0 is a line, in plane-0 that intersects the line
    # R1, V1 is a line, in plane-1 that intersects the line
    # Rs0 is a point on the line and on plane-0
    # Rs0, R1, V1 define a plane

    T0 = augmented_points[0][0]
    T1 = augmented_points[1][0]

    for t0 in range(1, T0 + 1):
        Rs0 = tuple(r + v * t0 for (r, v) in zip(R0, V0))
        # n1 is perpendicular to the plane defined by L1 and Rs0 -- should contain line
        n1 = cross(vsub(Rs0, R1), vsub(Rs0, vadd(R1, V1)))
        N = None
        for R, V in points[2:]:
            if N is None:
                # n1 is perpendicular to the plane defined by L2 and Rs0 -- should contain line
                n2 = cross(vsub(Rs0, R), vsub(Rs0, vadd(R, V)))
                # n is perpendicular to n0 and n1 and should be aligned with line
                n = cross(n1, n2)
                if dot(n, n) < 1e-3:
                    continue
                N = n
            # print(t0, N)
            metric = dot(cross(N, V), vsub(Rs0, R))
            if abs(metric) > 1e-3:
                N = None
                break
        if N is not None:
            break
    else:
        raise ValueError("couldn't find compatible normal")

    for t1 in range(1, T1 + 1):
        if t1 == t0:
            continue
        x0, y0, z0 = Rs0
        if t1 == t0:
            continue
        x1, y1, z1 = (r + v * t1 for (r, v) in zip(R1, V1))
        dt = t1 - t0
        vx = (x1 - x0) / dt
        vy = (y1 - y0) / dt
        vz = (z1 - z0) / dt
        # if abs(vx) < 0 or abs(vy) < 0 or abs(vz) < 0:
        #     break
        if not all(close(x - round(x), 0) for x in (vx, vy, vz)):
            continue
        V = (vx, vy, vz)
        R = tuple((r - v * t0 for (r, v) in zip((x0, y0, z0), V)))

        # x2 = r2_x + t2 * v2_x = Rx + vx * t2 => t2 = (r2_x - Rx) / (vx - v2_x)
        if V[0] == V2[0]:
            continue
        t2 = (R2[0] - R[0]) / (V[0] - V2[0])
        if not close(t2 - round(t2), 0):
            continue
        # assert t2 <= T2
        # for t2 in range(trials):
        x2, y2, z2 = (r + v * t2 for (r, v) in zip(R2, V2))
        x, y, z = (r + v * (t2 - t1) for (r, v) in zip((x1, y1, z1), V))
        if all(close(a, b) for (a, b) in zip([x2, y2, z2], [x, y, z])):
            return R, V
    raise RuntimeError("couldn't find value from normal :-(")


def intersecting_rock_coordinates_4(points, max_tries):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3


    p2 = r2 + v2 t
    p3 = ....


    """

    R0, V0 = points[0]
    R1, V1 = points[1]

    for total_v in range(1, max_tries):
        # if total_v % 100 == 0:
        # print("total_v =", total_v)
        for vx in range(-total_v, total_v + 1):
            for vy in range(-total_v, total_v + 1):
                for vz in range(-total_v, total_v + 1):
                    if abs(vx) + abs(vy) + abs(vz) != total_v:
                        continue
                    if vx == vy == vz == 0:
                        continue
                    V = (vx, vy, vz)
                    N0 = cross(
                        V, V0
                    )  # This is normal to a plane containing the line and R0
                    if is_null(N0):
                        continue
                    n0 = norm(N0)
                    h0 = dot(n0, R0)
                    N1 = cross(
                        V, V1
                    )  # This is normal to a plane containing the line and R1
                    if is_null(N1):
                        continue
                    n1 = norm(N1)
                    h1 = dot(n1, R1)

                    dot_n0n1 = dot(n0, n1)
                    denominator = 1 - dot_n0n1**2
                    if denominator == 0:
                        continue

                    c0 = (h0 - h1 * dot_n0n1) / denominator
                    c1 = (h1 - h0 * dot_n0n1) / denominator

                    Ra = vadd(scale(n0, c0), scale(n1, c1))

                    # Check if Ra is in our plane:
                    for Ri, Vi in points[2:]:
                        Ni = cross(
                            V, Vi
                        )  # This is normal to a plane containing the line and R2
                        if is_null(Ni):
                            continue
                        n = norm(Ni)
                        h = dot(n, Ri)
                        if not close(dot(Ra, n), h):
                            break
                    else:
                        Rint = as_integral(intersection(Ra, V, R0, V0))

                        # TODO: at this point we now we just need to scale V
                        # by N so can speed up there.

                        # print("found plausible speed")
                        t0 = (Rint[0] - R0[0]) / V0[0]

                        R = vsub(Rint, scale(V, t0))

                        for Ri, Vi in points[2:]:
                            Rint_i = intersection(Ra, V, Ri, Vi)
                            t_i_1 = (Rint_i[0] - Ri[0]) / Vi[0]
                            t_i_2 = (Rint_i[0] - R[0]) / V[0]
                            if not close(t_i_1, t_i_2):
                                break
                        else:
                            return R, V


def find_intersections(points):
    for i, (P1, V1) in enumerate(points):
        for j, (P2, V2) in enumerate(points[i + 1 :]):
            N = cross(V1, V2)
            if not close(mag2(N), 0) and close(dot(N, vsub(P1, P2)), 0):
                yield (P1, V1, P2, V2)


def find_plane(P1, V1, P2, V2):
    N = cross(V1, V2)
    if is_null(N):
        return None
    N = norm(N)
    h = dot(N, P1)
    return N, h


def argmax(A):
    return max(range(len(A)), key=lambda i: A[i])


def intersecting_rock_coordinates_5(points, max_tries):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3


    p2 = r2 + v2 t
    p3 = .sd...


    """

    N0 = None
    for P1, V1, P2, V2 in find_intersections(points):
        N, h = find_plane(P1, V1, P2, V2)
        # print(N, h)
        assert close(dot(N, P1), h)
        assert close(dot(N, P2), h)
        if N0 is None:
            N0, h0 = N, h
        else:
            if close(dot(N, N0), 1):
                continue
            N1, h1 = N, h

            dot_nn = dot(N0, N1)
            denominator = 1 - dot_nn**2
            c0 = (h0 - h1 * dot_nn) / denominator
            c1 = (h1 - h0 * dot_nn) / denominator

            # print(c0, c1)

            V = cross(N0, N1)

            Ra = vadd(scale(N0, c0), scale(N1, c1))
            # print(V)

            for i, (Ri, Vi) in enumerate(points):
                try:
                    Rint = as_integral(intersection(Ra, V, Ri, Vi))
                    # print(i, V, Rint)
                    j = argmax([abs(x) for x in Vi])
                    t0 = (Rint[j] - Ri[j]) / Vi[j]
                    # print(t0)
                    R = vsub(Rint, scale(V, t0))
                    # print(R)
                except (ZeroDivisionError, ValueError):
                    pass

        # Ni = cross(V, Vi)  # This is normal to a plane containing the line and R2
        # if is_null(Ni):
        #     continue
        # n = norm(Ni)
        # h = dot(n, Ri)
        # if not close(dot(Ra, n), h):
        #     break

    # print(Ra, V, Ri, Vi)
    # Rint = intersection(Ra, V, Ri, Vi)

    # print(Rint)


def intersecting_rock_coordinates_7(points, trials=10):
    """
     r1 + v1 t1 + v0 (t3 - t1) = r2 + v2 t2 + v0 (t2 - t1) = r3 + v3 t3


    p2 = r2 + v2 t
    p3 = ....


    79495361712 ???
    """

    # numbers = []
    # for X, V in points:
    #     numbers.extend(X)
    # print(math.gcd(*[int(x) for x in numbers]))

    # return [1, 2, 3], [4, 5, 6]

    augmented_points = []
    for X, V in points:
        *_, z = X
        assert z > 0
        *_, vz = V
        if vz >= 0:
            t_0 = inf
        else:
            t_0 = int(ceil(-z / vz))
        augmented_points.append((t_0, X, V))
    augmented_points.sort()
    # points = [x[1:] for x in augmented_points]

    R0, V0 = points[0]
    R1, V1 = points[1]
    R2, V2 = points[2]

    # R0, V0 is a line, in plane-0 that intersects the line
    # R1, V1 is a line, in plane-1 that intersects the line
    # Rs0 is a point on the line and on plane-0
    # Rs0, R1, V1 define a plane

    T0 = augmented_points[0][0]

    def compute_N(t0):
        Rs0 = tuple(r + v * t0 for (r, v) in zip(R0, V0))
        # n1 is perpendicular to the plane defined by L1 and Rs0 -- should contain line
        n1 = cross(vsub(Rs0, R1), vsub(Rs0, vadd(R1, V1)))
        N = None
        metric = 0
        for R, V in points[2:]:
            if N is None:
                # n1 is perpendicular to the plane defined by L2 and Rs0 -- should contain line
                n2 = cross(vsub(Rs0, R), vsub(Rs0, vadd(R, V)))
                # n is perpendicular to n0 and n1 and should be aligned with line
                n = cross(n1, n2)
                if dot(n, n) < 1e-3:
                    continue
                N = n
            metric += (dot(cross(N, V), vsub(Rs0, R))) ** 2
        return N, metric

    t_low = 1
    t_high = 100000 * int(T0)
    _, low = compute_N(t_low)
    _, high = compute_N(t_high)
    while t_low < t_high:
        t_0 = (t_low + t_high) // 2
        N, metric = compute_N(t_0)
        # print(">>>", metric)
        if metric < 1e-3:
            break
        if low < high:
            t_high = t_0
            high = metric
        else:
            t_low = t_0
            low = metric

    if metric > 1e-3:
        raise ValueError("couldn't find compatible normal")

    # print("Looking for second points at", t_0)

    P0int = tuple(r + v * t_0 for (r, v) in zip(R0, V0))
    P2int = as_integral(intersection(P0int, N, R2, V2))
    x0, y0, z0 = P0int

    # x1, y1, z1 = (r + v * t1 for (r, v) in zip(R1, V1))
    # dt = t1 - t0
    x2, y2, z2 = P2int
    for i, dx in enumerate(V2):
        if dx != 0:
            t_2 = round((P2int[i] - R2[i]) / dx)
            break
    dt = t_2 - t_0
    vx = (x2 - x0) / dt
    vy = (y2 - y0) / dt
    vz = (z2 - z0) / dt
    V = as_integral((vx, vy, vz))

    # print(P2int)
    # print(P0int)
    # print(V)
    # print(dt, t_2, t_0)
    R = tuple((r - v * t_0 for (r, v) in zip((x0, y0, z0), V)))

    return R, None


# 6:58


def intersection(p1, v1, p2, v2):
    # https://web.archive.org/web/20180927042445/http://mathforum.org/library/drmath/view/62814.html
    # a (V1 X V2) = (P2 - P1) X V2
    # L1 = P1 + a V1
    # => a = ((p2 - p1) x v2) . (v1 x v2) / |(v1 x v2)|**2
    v1xv2 = cross(v1, v2)
    a = dot(cross(vsub(p2, p1), v2), v1xv2) / dot(v1xv2, v1xv2)
    return vadd(p1, scale(v1, a))


def mag2(A):
    return dot(A, A)


def scale(A, s):
    a0, a1, a2 = A
    return (s * a0, s * a1, s * a2)


def vclose(A, B):
    return all(close(a, b) for (a, b) in zip(A, B))


def vadd(A, B):
    a0, a1, a2 = A
    b0, b1, b2 = B
    return (a0 + b0, a1 + b1, a2 + b2)


def vsub(A, B):
    a0, a1, a2 = A
    b0, b1, b2 = B
    return (a0 - b0, a1 - b1, a2 - b2)


def dot(A, B):
    a0, a1, a2 = A
    b0, b1, b2 = B
    return a0 * b0 + a1 * b1 + a2 * b2


def cross(A, B):
    a0, a1, a2 = A
    b0, b1, b2 = B
    return (a1 * b2 - a2 * b1, a2 * b0 - a0 * b2, a0 * b1 - a1 * b0)


def is_null(A):
    a0, a1, a2 = A
    return a0 == a1 == a2 == 0


def as_integral(A):
    if not all(close(a, round(a)) for a in A):
        raise ValueError(A)
    return tuple(int(round(a)) for a in A)


def norm(A):
    a0, a1, a2 = A
    mag = (a0**2 + a1**2 + a2**2) ** 0.5
    return (a0 / mag, a1 / mag, a2 / mag)


# -3, 1, 2
def part_2(text, max_tries=100000):
    """
    >>> part_2(EXAMPLE_TEXT, max_tries=20)
    47

    # 885680103420583 is too high
    """
    points = list(parse(text))
    R, V = intersecting_rock_coordinates_7(points, max_tries)
    return sum(R)
    # return intersecting_rock_coordinates_7(points, max_tries)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
