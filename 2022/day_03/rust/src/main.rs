use itertools::Itertools;
use std::collections::HashSet;
use std::env;
use std::fs;

fn load_rucksacks(path: &String) -> Vec<String> {
    let text = fs::read_to_string(path).expect("Should have been able to read the file");
    let mut rucksacks = Vec::new();
    for line in text.trim().split("\n") {
        rucksacks.push(line.to_string());
    }
    return rucksacks;
}

fn split_into_compartments(rucksacks: &Vec<String>) -> Vec<(String, String)> {
    let mut compartments = Vec::new();
    for line in rucksacks {
        let half = line.len() / 2;
        compartments.push((line[..half].to_string(), line[half..].to_string()));
    }
    return compartments;
}

fn find_duplicates(compartments: &Vec<(String, String)>) -> Vec<char> {
    let mut duplicates = Vec::new();
    for (c1, c2) in compartments {
        let set_1: HashSet<char> = c1.chars().collect();
        let set_2: HashSet<char> = c2.chars().collect();
        for (i, v) in set_1.intersection(&set_2).enumerate() {
            if i > 0 {
                panic!("crash and burn")
            }
            duplicates.push(*v)
        }
    }
    return duplicates;
}

fn total_score(items: &Vec<char>) -> i64 {
    let mut total_score = 0;
    for x_ref in items {
        let x = *x_ref;
        if x >= 'a' && x <= 'z' {
            total_score += x as i64 - 'a' as i64 + 1
        } else if x >= 'A' && x <= 'Z' {
            total_score += x as i64 - 'A' as i64 + 27
        } else {
            panic!("crash and burn")
        }
    }
    return total_score;
}

fn as_triples(rucksacks: &Vec<String>) -> Vec<(String, String, String)> {
    let mut triples = Vec::new();
    let mut tuples = rucksacks.into_iter().tuples();
    for (a, b, c) in tuples.by_ref() {
        triples.push((String::from(a), String::from(b), String::from(c)))
    }
    for _ in tuples.into_buffer() {
        panic!("there should be no leftovers")
    }
    return triples;
}

fn find_triplicates(items: &Vec<(String, String, String)>) -> Vec<char> {
    let mut triplicates = Vec::new();
    for (c1, c2, c3) in items {
        let set_1: HashSet<char> = c1.chars().collect();
        let set_2: HashSet<char> = c2.chars().collect();
        let set_3: HashSet<char> = c3.chars().collect();
        let set_12: HashSet<char> = set_1.intersection(&set_2).map(|x| *x).collect();
        for (i, v) in set_12.intersection(&set_3).enumerate() {
            if i > 0 {
                panic!("crash and burn")
            }
            triplicates.push(*v)
        }
    }
    return triplicates;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let rucksacks = load_rucksacks(path);

    let priority_score = total_score(&find_duplicates(&split_into_compartments(&rucksacks)));
    println!("priority score: {priority_score}");

    let badge_score = total_score(&find_triplicates(&as_triples(&rucksacks)));
    println!("badge score: {badge_score}")
}
