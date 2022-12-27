use crate::rustimp::Packet;
use core::cmp::Ordering::Less;

use std::env;
use std::error::Error;
use std::fs;
use std::process;

#[allow(unused_imports)]
use rustimp;

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

    let pairs = rustimp::load_packet_pairs(&text);

    let n: i64 = pairs
        .iter()
        .enumerate()
        .filter(|(_, (a, b))| Packet::cmp(a, b) == Less)
        .map(|(i, _)| i as i64 + 1)
        .sum();

    println!("{n}");

    let k = rustimp::find_decoder_key(&pairs);
    println!("{k}");
}
