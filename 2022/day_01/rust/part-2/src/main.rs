use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("In file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut calorie_list = Vec::new();
    let mut calories = 0;
    for line in contents.split("\n") {
        if line.trim().len() > 0 {
            calories += line.parse::<i64>().unwrap();
        } else {
            calorie_list.push(calories);
            calories = 0

        }
    }
    calorie_list.sort();

    let top3_calories:i64 = calorie_list[calorie_list.len() - 3..calorie_list.len()].iter().sum();
    println!("Max calories: {top3_calories}");
}