use crate::day_11::compute_business;
use day_11::load_monkeys;
use std::error::Error;
use std::fs;
use std::process;

use std::env;

#[allow(unused_imports)]
use day_11;

struct Config {
    path: String,
}

impl Config {
    fn new(args: Vec<String>) -> Result<Self, &'static str> {
        match args.len() {
            0 | 1 => Err("not enough arguments"),
            2 => Ok(Config {
                path: args[1].clone(),
            }),
            _ => Err("too many arguments"),
        }
    }
}

fn load_text(path: &String) -> Result<String, Box<dyn Error>> {
    Ok(fs::read_to_string(path)?)
}

fn main() {
    let args = env::args().collect();

    let config = Config::new(args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    let text = load_text(&config.path).unwrap_or_else(|err| {
        println!("Problem reading text: {err}");
        process::exit(1);
    });

    let answer_1 = compute_business(&mut load_monkeys(&text, 3), 20);
    println!("{answer_1}");
    let answer_1 = compute_business(&mut load_monkeys(&text, 1), 10000);
    println!("{answer_1}");
}
