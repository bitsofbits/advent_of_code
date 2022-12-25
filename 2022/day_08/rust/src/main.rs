use core::cmp::max;
use std::env;
use std::fs;

struct LowBudget2DArray<T> {
    data: Vec<T>,
    shape: (usize, usize),
}

impl<T> LowBudget2DArray<T> {
    fn new(data: Vec<T>, shape: (usize, usize)) -> Self {
        assert!(
            shape.0 * shape.1 == data.len(),
            "data length should match shape product"
        );
        LowBudget2DArray { data, shape }
    }

    fn index(&self, ndx: (usize, usize)) -> &T {
        assert!(ndx.0 < self.shape.0, "ndx.0 should be in bounds");
        assert!(ndx.1 < self.shape.1, "ndx.1 should be in bounds");
        &self.data[ndx.0 * self.shape.1 + ndx.1]
    }
}

impl<T: std::fmt::Display> std::fmt::Display for LowBudget2DArray<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for row in 0..self.shape.0 {
            let row = &self.data[row * self.shape.0..(row + 1) * self.shape.1];
            let txt = row
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<String>>()
                .join("");
            write!(f, "{}\n", txt).expect("array should print");
        }
        Ok(())
    }
}

fn find_visibility_distance(
    hmap: &LowBudget2DArray<i32>,
    ndx: (usize, usize),
    direction: usize,
) -> (i32, bool) {
    let delta: (i32, i32) = vec![(1, 0), (-1, 0), (0, 1), (0, -1)][direction];
    let max_ndx = vec![hmap.shape.0, hmap.shape.0, hmap.shape.1, hmap.shape.1][direction];

    let base_height = hmap.index(ndx);
    let shape = (hmap.shape.0 as i32, hmap.shape.1 as i32);
    let mut ndx: (i32, i32) = (ndx.0 as i32, ndx.1 as i32);
    for i in 0..max_ndx {
        ndx = (ndx.0 + delta.0, ndx.1 + delta.1);
        if ndx.0 < 0 || ndx.0 >= shape.0 || ndx.1 < 0 || ndx.1 >= shape.1 {
            return (i as i32, true);
        }
        let height = hmap.index((ndx.0 as usize, ndx.1 as usize));
        if height >= base_height {
            return (i as i32, false);
        }
    }
    panic!("should have returned earlier");
}

fn find_visible(hmap: &LowBudget2DArray<i32>, ndx: (usize, usize)) -> bool {
    let mut visible = false;
    for direction in 0..4 {
        let (dist, _) = find_visibility_distance(&hmap, ndx, direction);
        match direction {
            0 => visible |= dist == (hmap.shape.0 - ndx.0 - 1).try_into().unwrap(),
            1 => visible |= dist == ndx.0.try_into().unwrap(),
            2 => visible |= dist == (hmap.shape.1 - ndx.1 - 1).try_into().unwrap(),
            3 => visible |= dist == ndx.1.try_into().unwrap(),
            _ => (),
        }
    }
    return visible;
}

fn visible_sum(hmap: &LowBudget2DArray<i32>) -> i32 {
    let mut total = 0;
    for i in 0..hmap.shape.0 {
        for j in 0..hmap.shape.1 {
            if find_visible(hmap, (i, j)) {
                total += 1
            }
        }
    }
    total
}

fn find_scenic_score(hmap: &LowBudget2DArray<i32>, ndx: (usize, usize)) -> i32 {
    let mut score = 1;
    for direction in 0..4 {
        let (dist, at_edge) = find_visibility_distance(hmap, ndx, direction);
        if at_edge {
            score *= dist;
        } else {
            score *= dist + 1;
        }
    }
    score
}

fn max_scenic_score(hmap: &LowBudget2DArray<i32>) -> i32 {
    let mut maxscore = 0;
    for i in 0..hmap.shape.0 {
        for j in 0..hmap.shape.1 {
            maxscore = max(find_scenic_score(hmap, (i, j)), maxscore);
        }
    }
    maxscore
}

fn load_map(path: &String) -> LowBudget2DArray<i32> {
    let text = fs::read_to_string(path).expect("Should have been able to read the file");
    let mut data = Vec::new();
    let mut rows = 0;
    for line in text.trim().split("\n") {
        data.extend(
            line.trim()
                .chars()
                .map(|x| x.to_string().parse::<i32>().unwrap()),
        );
        rows += 1;
    }
    let cols = data.len() / rows;
    LowBudget2DArray::new(data, (rows, cols))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let heights = load_map(path);
    let visible = visible_sum(&heights);
    println!("{visible}");
    let max_scenic_score = max_scenic_score(&heights);
    println!("{max_scenic_score}");
}
