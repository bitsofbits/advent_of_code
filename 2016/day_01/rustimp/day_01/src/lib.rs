use std::collections::HashSet;

fn parse(text: &str) -> Vec<(char, isize)> {
    let mut vec = Vec::new();
    for x in text.trim().split(", ") {
        vec.push((x.chars().next().unwrap(), x[1..].parse().unwrap()));
    }
    return vec;
}

fn to_grid(n: isize, angle: isize) -> (isize, isize) {
    return {
        match angle {
            0 => (0, n),
            90 => (n, 0),
            180 => (0, -n),
            270 => (-n, 0),
            _ => panic!("illegal angle: {}", angle),
        }
    };
}

pub fn solve_1(text: &String) -> isize {
    let mut x = 0;
    let mut y = 0;
    let mut angle = 0;
    for (turn, dist) in parse(&text) {
        match turn {
            'R' => angle += 90,
            'L' => angle += 270,
            _ => panic!("illegal direction: {}", angle),
        }
        angle %= 360;
        let (dx, dy) = to_grid(dist, angle);
        x += dx;
        y += dy;
    }
    x.abs() + y.abs()
}

pub fn solve_2(text: &String) -> isize {
    let mut x = 0;
    let mut y = 0;
    let mut angle = 0;
    let mut visited = HashSet::from([(x, y)]);
    for (turn, dist) in parse(&text) {
        match turn {
            'R' => angle += 90,
            'L' => angle += 270,
            _ => panic!("illegal direction: {}", angle),
        }
        angle %= 360;
        let (dx, dy) = to_grid(dist, angle);
        for _ in 0..dx.abs().max(dy.abs()) {
            x += dx.signum();
            y += dy.signum();
            if visited.contains(&(x, y)) {
                return x.abs() + y.abs();
            }
            visited.insert((x, y));
        }
    }
    panic!("didn't find a solution");
}
