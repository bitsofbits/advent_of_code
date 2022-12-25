use std::cmp::max;
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("In file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut max_calories = 0;
    let mut calories = 0;
    for line in contents.split("\n") {
        if line.trim().len() > 0 {
            calories += line.parse::<i64>().unwrap();
        } else {
            max_calories = max(max_calories, calories);
            calories = 0

        }

    }

    println!("Max calories: {max_calories}");
}