use itertools::Itertools;
use std::collections::HashMap;

fn make_i64(text: &str) -> i64 {
    text.trim().parse::<i64>().unwrap()
}

fn make_u64(text: &str) -> u64 {
    text.trim().parse::<u64>().unwrap()
}

fn trim(text: &str) -> String {
    (*text.trim()).to_string()
}
#[derive(Debug)]
enum Op {
    Square,
    Add(i64),
    Mult(i64),
}
impl Op {
    fn from_text(text: &str) -> Self {
        match text.split(" ").collect_tuple().unwrap() {
            ("old", "*", "old") => Op::Square,
            ("old", "*", arg) => Op::Mult(make_i64(arg)),
            ("old", "+", arg) => Op::Add(make_i64(arg)),
            _ => panic!("unknown op"),
        }
    }
    fn apply(&self, x: &u64) -> u64 {
        match self {
            Op::Square => x * x,
            Op::Add(arg) => x + (*arg as u64),
            Op::Mult(arg) => x * (*arg as u64),
        }
    }
}

type Ident = u64;
type Worry = u64;

#[derive(Debug)]
pub struct Monkey {
    identifier: Ident,
    operation: Op,
    test_value: u64,
    true_target: Ident,
    false_target: Ident,
    items: Vec<Worry>,
    relief_factor: u64,
    inspections: u64,
}

impl Monkey {
    fn take_turn(&mut self, modulus: u64) -> Vec<(Ident, Worry)> {
        let mut targets = Vec::new();
        for x in &self.items {
            self.inspections += 1;
            let x = self.operation.apply(x);
            let x = (x / self.relief_factor) % modulus;
            if x % self.test_value == 0 {
                targets.push((self.true_target, x))
            } else {
                targets.push((self.false_target, x))
            }
        }
        self.items.clear();
        targets
    }
    fn modulus(monkeys: &HashMap<Ident, Monkey>) -> u64 {
        let mut modulus = 1;
        for (_, m) in monkeys {
            modulus *= m.test_value
        }
        modulus
    }
    fn play_round(monkeys: &mut HashMap<u64, Monkey>) {
        let modulus = Monkey::modulus(&monkeys);
        for k in monkeys.iter().map(|(k, _)| k.clone()).sorted() {
            let m = monkeys.get_mut(&k).unwrap();
            let targets = m.take_turn(modulus);
            for (kt, vt) in targets {
                monkeys.get_mut(&kt).unwrap().items.push(vt);
            }
        }
    }

    fn from_text(text: &str, relief_factor: u64) -> Self {
        let text = text.trim();
        let lines: Vec<&str> = text.split("\n").collect();
        assert!(lines.len() == 6);
        let identifier = extract_from(lines[0], "Monkey", ":", &make_u64);
        let items = extract_from(lines[1], "Starting items:", "", &trim);
        let items = items.split(",").map(|x| make_u64(x.trim())).collect();
        let operation = extract_from(lines[2], "Operation: new =", "", &Op::from_text);
        let test_value = extract_from(lines[3], "Test: divisible by", "", &make_u64);
        let true_target = extract_from(lines[4], "If true: throw to monkey", "", &make_u64);
        let false_target = extract_from(lines[5], "If false: throw to monkey", "", &make_u64);
        Monkey {
            identifier,
            operation,
            test_value,
            true_target,
            false_target,
            items,
            relief_factor,
            inspections: 0,
        }
    }
}

fn extract_from<T>(line: &str, prefix: &str, suffix: &str, factory: &dyn Fn(&str) -> T) -> T {
    let line = line.trim();
    let n = prefix.len();
    assert!(&line[..n] == prefix, "{line}");
    let line = &line[n..];
    let n = line.len() - suffix.len();
    assert!(&line[n..] == suffix, "{line}");
    let line = &line[..n];
    factory(line.trim())
}

pub fn compute_business(monkeys: &mut HashMap<Ident, Monkey>, rounds: u64) -> u64 {
    for _ in 0..rounds {
        Monkey::play_round(monkeys);
    }
    let mut ordered: Vec<(Ident, &Monkey)> = monkeys
        .iter()
        .map(|(k, v)| (k.clone(), v.clone()))
        .collect();
    ordered.sort_by(|(_, v1), (_, v2)| v1.inspections.partial_cmp(&v2.inspections).unwrap());
    let n = ordered.len();
    ordered[n - 1].1.inspections * ordered[n - 2].1.inspections
}

pub fn load_monkeys(text: &str, relief_factor: u64) -> HashMap<Ident, Monkey> {
    let mut monkeys: Vec<Monkey> = text
        .split("\n\n")
        .map(|x| Monkey::from_text(x, relief_factor))
        .collect();
    HashMap::from_iter(monkeys.drain(..).map(|x| (x.identifier, x)))
}
