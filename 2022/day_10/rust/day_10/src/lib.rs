#[derive(Debug)]
pub enum Command {
    Addx(i32),
    Noop,
}

pub fn parse_program(text: &String) -> Vec<Command> {
    let mut commands = Vec::new();
    for line in text.lines() {
        match line.trim().split(" ").collect::<Vec<&str>>()[..] {
            ["addx", arg] => commands.push(Command::Addx(arg.parse::<i32>().unwrap())),
            ["noop"] => commands.push(Command::Noop),
            _ => panic!("illegal command"),
        }
    }
    commands
}

pub fn execute_program(program: Vec<Command>) -> Vec<(usize, i32)> {
    let mut x = 1;
    let mut cycle = 0;
    let mut states = Vec::new();
    for op in program {
        match op {
            Command::Noop => {
                cycle += 1;
                states.push((cycle, x));
            }
            Command::Addx(arg) => {
                cycle += 1;
                states.push((cycle, x));
                cycle += 1;
                states.push((cycle, x));
                x += arg;
            }
        }
    }
    states
}

pub fn sum_signal(states: &Vec<(usize, i32)>) -> i32 {
    let mut total = 0;
    let probe_cycles = vec![20, 60, 100, 140, 180, 220];
    for (cycle, value) in states {
        if probe_cycles.contains(&cycle) {
            total += value * (*cycle as i32)
        }
    }
    total
}

pub fn rasterize(states: &Vec<(usize, i32)>) -> String {
    let mut string = String::from("");
    for (cycle, value) in states {
        let ndx = cycle - 1;
        if ndx > 0 && ndx % 40 == 0 {
            string.push_str("\n");
        }
        let col = (ndx % 40) as i32;
        let is_lit = value - 1 <= col && col <= value + 1;
        string.push(if is_lit { '#' } else { '.' });
    }
    string
}
