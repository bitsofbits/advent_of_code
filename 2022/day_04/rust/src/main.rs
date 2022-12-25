use itertools::Itertools;
use std::collections::HashSet;
use std::env;
use std::fs;

fn as_set(text: &String) -> HashSet<i32> {
    let (a, b) = text.split("-").collect_tuple().unwrap();
    let i = a.parse::<i32>().unwrap();
    let j = b.parse::<i32>().unwrap();
    return HashSet::<i32>::from_iter(i..=j);
}

fn load_assignments(path: &String) -> Vec<(HashSet<i32>, HashSet<i32>)> {
    let text = fs::read_to_string(path).expect("Should have been able to read the file");
    let mut assignments = Vec::new();
    for line in text.trim().split("\n") {
        let (left, right) = line.trim().split(",").collect_tuple().unwrap();
        assignments.push((as_set(&left.to_string()), as_set(&right.to_string())));
    }
    return assignments;
}

fn is_contained(sets: &(HashSet<i32>, HashSet<i32>)) -> bool {
    let (a, b) = sets;
    return a.difference(b).collect::<HashSet<&i32>>().is_empty()
        || b.difference(a).collect::<HashSet<&i32>>().is_empty();
}

fn is_overlapping(sets: &(HashSet<i32>, HashSet<i32>)) -> bool {
    let (a, b) = sets;
    return !a.intersection(b).collect::<HashSet<&i32>>().is_empty();
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let assignments = load_assignments(path);

    let n_contained = assignments
        .iter()
        .map(|x| is_contained(x) as i32)
        .sum::<i32>();
    println!("number completely contained: {n_contained:?}");

    let n_overlapping = assignments
        .iter()
        .map(|x| is_overlapping(x) as i32)
        .sum::<i32>();
    println!("number of overlaps: {n_overlapping:?}");
}
