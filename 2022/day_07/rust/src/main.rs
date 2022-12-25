use itertools::Itertools;
use std::collections::HashMap;
use std::env;
use std::fs;

fn load_input(path: &String) -> String {
    fs::read_to_string(path).expect("Should have been able to read the file")
}

fn process_cmd(line: &str, mut path: Vec<String>) -> (Vec<String>, bool) {
    assert!(line.starts_with("$ "), "incorrect command format");
    let line = line[2..].trim();
    if line == "ls" {
        return (path, true);
    } else {
        let (cmd, arg) = line.split(" ").collect_tuple().expect("malformed line");
        if cmd == "cd" {
            if arg == "/" {
                path.clear();
                path.push("/".to_string());
            } else if arg == ".." {
                path.pop();
            } else {
                assert!(!arg.contains("/"), "paths should not contain /");
                path.push(arg.to_string())
            }
            return (path, false);
        } else {
            panic!("unknown command")
        }
    }
}

fn process_listing(line: &str) -> (String, i32) {
    let (sizestr, name) = line
        .trim()
        .split(" ")
        .collect_tuple()
        .expect("tuple should be well formed");
    let mut size = 0;
    if sizestr != "dir" {
        size = sizestr.parse::<i32>().unwrap()
    }
    return (name.to_string(), size);
}

fn process_commands(text: &String) -> HashMap<String, Vec<(String, i32)>> {
    let mut path: Vec<String> = Vec::new();
    let mut dirs: HashMap<String, Vec<(String, i32)>> = HashMap::new();
    let mut expect_data = false;
    for line in text.trim().split("\n") {
        if line.starts_with("$") {
            (path, expect_data) = process_cmd(line, path);
        } else {
            assert!(expect_data == true, "unexpected data");
            let key = path.join("/");
            if !dirs.contains_key(&key) {
                dirs.insert(key.clone(), Vec::new());
            }
            dirs.get_mut(&key)
                .expect("should have key")
                .push(process_listing(&line))
        }
    }

    return dirs;
}

fn find_size(path: &str, dirs: &HashMap<String, Vec<(String, i32)>>) -> i32 {
    let mut size = 0;
    for (name, mut sz) in &dirs[&*path] {
        if sz == 0 {
            let subpath = format!("{path}/{name}");
            sz = find_size(&subpath, dirs);
        }
        size += sz;
    }
    return size;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = &args[1];

    let input = load_input(path);
    let dirs = process_commands(&input);

    let total_small: i32 = dirs
        .iter()
        .map(|(k, _)| find_size(k, &dirs))
        .filter(|x| x <= &100000i32)
        .sum();
    println!("{total_small}");

    let total_space = 70000000;
    let needed = 30000000;
    let must_delete = needed - (total_space - find_size("/", &dirs));
    let mut sizes: Vec<i32> = dirs.iter().map(|(k, _)| find_size(k, &dirs)).collect();
    sizes.sort_by(|a, b| a.cmp(b));
    let ndx = sizes.partition_point(|x| x < &must_delete);
    let size_of_dir_to_delete = sizes[ndx];
    println!("{size_of_dir_to_delete}");
}
