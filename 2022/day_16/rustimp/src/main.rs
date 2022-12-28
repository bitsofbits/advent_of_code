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

    let nodes = rustimp::Node::parse_graph(&text);
    let (mut nodes, root) = rustimp::Node::from_string_based_graph(nodes, "AA");
    nodes = rustimp::add_all_paths(nodes);
    nodes = rustimp::drop_nodes_with_zero_flow(nodes, root);
    let n = rustimp::traverse(&nodes, &root);
    println!("{n}");
    let n = rustimp::dual_traverse(&nodes, &root);
    println!("{n}");
}
