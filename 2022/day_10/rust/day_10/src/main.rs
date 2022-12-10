use std::error::Error;
use std::fs;
use std::process;

use std::env;

#[allow(unused_imports)]
use day_10;

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

    let program = day_10::parse_program(&text);
    let states = day_10::execute_program(program);
    let total_signal = day_10::sum_signal(&states);
    println!("{total_signal}");
    let raster = day_10::rasterize(&states);
    println!("{raster}");
}
