use std::collections::HashSet;
use std::collections::VecDeque;
use std::env;
use std::fs;

fn load_input(path: &String) -> String {
    fs::read_to_string(path).expect("Should have been able to read the file")
}

fn find_unique_run_location(txt: &String, run_length: usize) -> usize {
    let mut prefix: VecDeque<char> = VecDeque::with_capacity(run_length);
    for (i, x) in txt.chars().enumerate() {
        prefix.push_back(x);
        if prefix.len() == run_length {
            let s: HashSet<&char> = HashSet::from_iter(&prefix);
            if s.len() == run_length {
                return i + 1;
            }
            prefix.pop_front();
        }
    }
    txt.len()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let input = load_input(path);
    let n = find_unique_run_location(&input, 4);
    println!("{n}");
    let n = find_unique_run_location(&input, 14);
    println!("{n}");
}
