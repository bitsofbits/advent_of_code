use itertools::Itertools;
use std::collections::HashSet;
use std::error::Error;

pub struct Move {
    direction: char,
    count: i32,
}

pub struct Rope {
    knots: Vec<(i32, i32)>,
}

impl Rope {
    pub fn new(n_knots: usize) -> Self {
        let knots: Vec<(i32, i32)> = vec![(0, 0); n_knots];
        Rope { knots }
    }

    fn update_knot(&mut self, i: usize) {
        let (x_h, y_h) = self.knots[i - 1];
        let (mut x_t, mut y_t) = self.knots[i];
        let dx = x_h - x_t;
        let dy = y_h - y_t;
        if dx.abs() > 1 || dy.abs() > 1 {
            x_t += dx.signum();
            y_t += dy.signum();
        }
        self.knots[i] = (x_t, y_t)
    }

    fn move_head(&mut self, direction: char) {
        let (mut x, mut y) = self.knots[0];
        match direction {
            'U' => y += 1,
            'D' => y -= 1,
            'R' => x += 1,
            'L' => x -= 1,
            _ => panic!("illegal directions"),
        }
        self.knots[0] = (x, y);
        for i in 1..self.knots.len() {
            self.update_knot(i)
        }
    }

    fn tail(&self) -> (i32, i32) {
        self.knots[self.knots.len() - 1]
    }
}

pub fn count_tail_locs(mut rope: Rope, moves: &Vec<Move>) -> usize {
    let mut tail_locs: HashSet<(i32, i32)> = HashSet::new();
    tail_locs.insert(rope.tail());
    for mv in moves {
        for _ in 0..mv.count {
            rope.move_head(mv.direction);
            tail_locs.insert(rope.tail());
        }
    }
    tail_locs.len()
}

// TODO: use result error handling instead
pub fn parse_moves(text: &str) -> Result<Vec<Move>, Box<dyn Error>> {
    let mut moves = Vec::new();
    for line in text.lines() {
        let line = line.trim();
        if !line.is_empty() {
            let (direction, count) = line.split(" ").collect_tuple().ok_or(line)?;
            let (direction,) = direction.chars().collect_tuple().ok_or(line)?;
            let count = count.parse::<i32>()?;
            moves.push(Move { direction, count });
        }
    }
    Ok(moves)
}
