use crate::day_9::count_tail_locs;
use crate::day_9::parse_moves;
use crate::day_9::Rope;
use std::error::Error;
use std::fs;
use std::process;

use std::env;

use day_9;

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

    let moves = parse_moves(&text).unwrap_or_else(|err| {
        println!("Could not parse moves: \"{err}\"");
        process::exit(1);
    });

    let locs = count_tail_locs(Rope::new(2), &moves);
    println!("{locs}");
    let locs = count_tail_locs(Rope::new(10), &moves);
    println!("{locs}");
}
