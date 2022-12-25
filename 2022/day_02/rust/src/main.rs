use itertools::Itertools;
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::env;
use std::fs;

const PLAY_SCORE: Lazy<HashMap<&str, i32>> =
    Lazy::new(|| HashMap::from([("X", 1), ("Y", 2), ("Z", 3)]));

const RESULTS: Lazy<HashMap<(&str, &str), i32>> = Lazy::new(|| {
    HashMap::from([
        (("A", "X"), 3),
        (("A", "Y"), 6),
        (("A", "Z"), 0),
        (("B", "Y"), 3),
        (("B", "Z"), 6),
        (("B", "X"), 0),
        (("C", "Z"), 3),
        (("C", "X"), 6),
        (("C", "Y"), 0),
    ])
});

const ME_MAP: Lazy<HashMap<(&str, &str), &str>> = Lazy::new(|| {
    HashMap::from([
        (("A", "X"), "Z"),
        (("A", "Y"), "X"),
        (("A", "Z"), "Y"),
        (("B", "X"), "X"),
        (("B", "Y"), "Y"),
        (("B", "Z"), "Z"),
        (("C", "X"), "Y"),
        (("C", "Y"), "Z"),
        (("C", "Z"), "X"),
    ])
});

fn load_guide(path: &String) -> Vec<String> {
    let text = fs::read_to_string(path).expect("Should have been able to read the file");
    let mut rucksacks = Vec::new();
    for line in text.trim().split("\n") {
        rucksacks.push(line.to_string());
    }
    return rucksacks;
}

fn compute_score_1(items: &Vec<String>) -> i32 {
    let mut total = 0;
    for line in items {
        if let Some((op, me)) = line.trim().split(" ").collect_tuple() {
            total += PLAY_SCORE[&me] + RESULTS[&(op, me)]
        } else {
            panic!("expected two elements")
        }
    }
    return total;
}

fn compute_score_2(items: &Vec<String>) -> i32 {
    let mut total = 0;
    for line in items {
        if let Some((op, result)) = line.trim().split(" ").collect_tuple() {
            let me = ME_MAP[&(op, result)];
            total += PLAY_SCORE[&me] + RESULTS[&(op, me)]
        } else {
            panic!("expected two elements")
        }
    }
    return total;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];
    let guide = load_guide(path);

    let score_1 = compute_score_1(&guide);
    println!("score1: {score_1}");

    let score_2 = compute_score_2(&guide);
    println!("score2: {score_2}");
}
