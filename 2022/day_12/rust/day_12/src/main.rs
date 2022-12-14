use day_12::Map;
use day_12::StartValue;
use std::error::Error;
use std::fs;
use std::process;

use std::env;

#[allow(unused_imports)]
use day_12;

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

    let answer_1 = Map::new(&text)
        .expect("map should load")
        .find_shortest_path(StartValue::Start)
        .len();
    println!("{answer_1}");
    let answer_2 = Map::new(&text)
        .expect("map should load")
        .find_shortest_path(StartValue::Value(0))
        .len();
    println!("{answer_2}");
}
