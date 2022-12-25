use itertools::Itertools;
use std::env;
use std::fs;

#[derive(Debug)]
struct Move {
    count: i32,
    source: usize,
    dest: usize,
}

fn parse_move(text: &str) -> Move {
    let (_, cnt, _, src, _, dst) = text.split(" ").collect_tuple().unwrap();
    return Move {
        count: cnt.parse::<i32>().unwrap(),
        source: src.parse::<usize>().unwrap() - 1,
        dest: dst.parse::<usize>().unwrap() - 1,
    };
}

fn parse_diagram(layers: Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut stacks = Vec::new();
    let indices: [usize; 9] = [1, 5, 9, 13, 17, 21, 25, 29, 33];
    for _ in 0..9 {
        stacks.push(Vec::new());
    }
    for (lyr_num, lyr) in layers.iter().enumerate() {
        if lyr_num == layers.len() - 1 {
            break;
        }
        for (i, ndx) in indices.iter().enumerate() {
            let c = lyr[*ndx];
            if c != ' ' {
                stacks[i].push(c)
            }
        }
    }
    for i in 0..9 {
        stacks[i].reverse()
    }
    return stacks;
}

fn load_inputs(path: &String) -> (Vec<Vec<char>>, Vec<Move>) {
    let text = fs::read_to_string(path).expect("Should have been able to read the file");
    let mut diagram_layers = Vec::new();
    let mut moves = Vec::new();
    let mut processing_diagram = true;
    for line in text.split("\n") {
        if processing_diagram {
            if line.trim().is_empty() {
                processing_diagram = false;
                continue;
            }
            diagram_layers.push(line.chars().collect())
        } else {
            if !line.trim().is_empty() {
                moves.push(parse_move(line))
            }
        }
    }
    return (parse_diagram(diagram_layers), moves);
}

fn apply_moves_cm9000(mut stacks: Vec<Vec<char>>, moves: &Vec<Move>) -> Vec<Vec<char>> {
    for m in moves {
        for _ in 0..m.count {
            let c = stacks[m.source].pop().expect("Should have items");
            stacks[m.dest].push(c);
        }
    }
    return stacks;
}

fn apply_moves_cm9001(mut stacks: Vec<Vec<char>>, moves: &Vec<Move>) -> Vec<Vec<char>> {
    for m in moves {
        let ndx = stacks[m.dest].len();
        for _ in 0..m.count {
            let c = stacks[m.source].pop().expect("Should have items");
            stacks[m.dest].insert(ndx, c);
        }
    }
    return stacks;
}

fn top_layer(stacks: Vec<Vec<char>>) -> String {
    let mut chars = Vec::new();
    for s in stacks {
        let c = *s.last().expect("stacks should have items");
        chars.push(c)
    }
    chars.into_iter().collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let (stacks, moves) = load_inputs(path);
    let top = top_layer(apply_moves_cm9000(stacks, &moves));
    println!("{top:?}");

    let (stacks, moves) = load_inputs(path);
    let top = top_layer(apply_moves_cm9001(stacks, &moves));
    println!("{top:?}");
}
