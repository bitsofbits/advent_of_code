use std::collections::HashMap;
use std::collections::HashSet;

pub struct Array2D<T> {
    data: Vec<T>,
    shape: (usize, usize),
}

impl<T> Array2D<T> {
    pub fn new(data: Vec<T>, shape: (usize, usize)) -> Self {
        assert!(
            shape.0 * shape.1 == data.len(),
            "data length should match shape product"
        );
        Array2D { data, shape }
    }

    pub fn in_bounds(&self, ndx: (usize, usize)) -> bool {
        return (ndx.0 < self.shape.0) && (ndx.1 < self.shape.1);
    }

    pub fn index(&self, ndx: (usize, usize)) -> &T {
        assert!(self.in_bounds(ndx), "ndx.1 should be in bounds");
        &self.data[ndx.0 * self.shape.1 + ndx.1]
    }
}

pub enum StartValue {
    Start,
    Value(u8),
}

pub struct Map {
    pub start: (usize, usize),
    pub end: (usize, usize),
    pub data: Array2D<u8>,
}

impl Map {
    pub fn new(text: &str) -> Option<Self> {
        let text = text.trim();
        let mut data = Vec::new();
        let mut width = 0;
        let mut i = 0;
        let mut start = Some((0, 0));
        let mut end = Some((0, 0));
        for line in text.split("\n") {
            let line = line.trim();
            if line.len() > 0 {
                if width == 0 {
                    width = line.len()
                }
                assert!(line.len() == width);
                for (j, &(mut c)) in line.as_bytes().iter().enumerate() {
                    match c {
                        b'S' => {
                            c = b'a';
                            start = Some((i, j))
                        }
                        b'E' => {
                            c = b'z';
                            end = Some((i, j))
                        }
                        _ => (),
                    }
                    data.push(c - b'a');
                }
                i += 1;
            }
        }
        let data = Array2D::new(data, (i, width));
        match (start, end) {
            (Some(start), Some(end)) => Some(Map { start, end, data }),
            _ => None,
        }
    }

    fn get_valid_neighbors(&self, pt: (usize, usize), reverse: bool) -> Vec<(usize, usize)> {
        let (i0, j0) = pt;
        let ch0 = self.data.index(pt);
        let mut neighbors = Vec::new();
        for (di, dj) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let (i1, j1) = ((i0 as i32) + di, (j0 as i32) + dj);
            if i1 < 0 || j1 < 0 {
                continue;
            }
            let pt1 = (i1 as usize, j1 as usize);
            if !self.data.in_bounds(pt1) {
                continue;
            }
            let ch1 = self.data.index(pt1);
            if reverse {
                if *ch0 as i32 - *ch1 as i32 <= 1 {
                    neighbors.push(pt1);
                }
            } else {
                if *ch1 as i32 - *ch0 as i32 <= 1 {
                    neighbors.push(pt1)
                }
            }
        }
        neighbors
    }

    fn sample_forward(
        &self,
        start_value: StartValue,
    ) -> ((usize, usize), Vec<((usize, usize), usize)>) {
        let mut nodes = vec![(self.end, 0)];
        let mut used_pts = HashSet::new();
        used_pts.insert(nodes[0].0);
        let mut i = 0;
        loop {
            let (pt0, counter) = nodes[i];
            for pt1 in self.get_valid_neighbors(pt0, true) {
                if used_pts.contains(&pt1) {
                    continue;
                };
                nodes.push((pt1, counter + 1));
                match start_value {
                    StartValue::Start => {
                        if pt1 == self.start {
                            return (pt1, nodes);
                        }
                    }
                    StartValue::Value(start_value) => {
                        if self.data.index(pt1) == &start_value {
                            return (pt1, nodes);
                        }
                    }
                }
                used_pts.insert(pt1);
            }
            i += 1
        }
    }

    fn sample_back(
        &self,
        start: (usize, usize),
        nodes: Vec<((usize, usize), usize)>,
    ) -> Vec<(usize, usize)> {
        let by_pt: HashMap<(usize, usize), usize> = nodes.iter().map(|(x, y)| (*x, *y)).collect();
        let mut pt = start;
        let mut path = Vec::new();
        loop {
            let mut candidates: Vec<(usize, usize)> = self
                .get_valid_neighbors(pt, false)
                .iter()
                .filter(|x| by_pt.contains_key(x))
                .map(|(x, y)| (*x, *y))
                .collect();
            candidates.sort_by(|x, y| {
                by_pt
                    .get(x)
                    .unwrap()
                    .partial_cmp(by_pt.get(y).unwrap())
                    .unwrap()
            });
            pt = candidates[0];
            path.push(pt);
            if pt == self.end {
                break;
            }
        }
        path
    }

    pub fn find_shortest_path(&self, start_value: StartValue) -> Vec<(usize, usize)> {
        let (start_pt, nodes) = self.sample_forward(start_value);
        self.sample_back(start_pt, nodes)
    }
}

#[test]
fn test_part1() {
    use std::fs;

    let input = fs::read_to_string("../../data/example.txt").unwrap();
    if let Some(map) = Map::new(&input) {
        let n = map.find_shortest_path(StartValue::Start).len();
        assert_eq!(n, 31);
    } else {
        panic!("could not build map")
    }
}

#[test]
fn test_part2() {
    use std::fs;

    let input = fs::read_to_string("../../data/example.txt").unwrap();
    if let Some(map) = Map::new(&input) {
        let n = map.find_shortest_path(StartValue::Value(0)).len();
        assert_eq!(n, 29);
    } else {
        panic!("could not build map")
    }
}
