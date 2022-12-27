use core::cmp::Ordering;
use core::cmp::Ordering::Equal;
use itertools::Itertools;
use nom::{bytes::complete::take_while1, combinator::map_res, IResult};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum Packet {
    Int(i64),
    List(Vec<Packet>),
}

impl Packet {
    pub fn cmp(a: &Self, b: &Self) -> Ordering {
        match (a, b) {
            (Packet::Int(x), Packet::Int(y)) => x.cmp(y),
            (Packet::List(_), Packet::Int(_)) => {
                return Packet::cmp(a, &Packet::List(vec![b.clone()]))
            }
            (Packet::Int(_), Packet::List(_)) => {
                return Packet::cmp(&Packet::List(vec![a.clone()]), b)
            }
            (Packet::List(l), Packet::List(m)) => {
                for (c, d) in l.iter().zip(m.iter()) {
                    let cmp = Packet::cmp(c, d);
                    if cmp != Equal {
                        return cmp;
                    }
                }
                return l.len().cmp(&m.len());
            }
        }
    }
}

fn from_int(input: &str) -> Result<i64, std::num::ParseIntError> {
    i64::from_str_radix(input, 10)
}

fn is_int_digit(c: char) -> bool {
    c.is_digit(10)
}

fn int_primary(input: &str) -> IResult<&str, i64> {
    map_res(take_while1(is_int_digit), from_int)(input)
}

fn csp_parser(text: &str) -> IResult<&str, Packet> {
    // Parse comma separated packets
    let mut packets = Vec::new();
    let mut i0 = 0;
    let mut i1 = 0;
    let mut chars = text.chars();
    let mut count = 0;
    while i1 < text.len() {
        let c = chars.next();
        i1 += 1;
        match (c.unwrap(), count) {
            ('[', _) => count += 1,
            (']', _) => count -= 1,
            (',', 0) => {
                let (_, p) = packet_parser(&text[i0..i1])?;
                packets.push(p);
                i0 = i1;
            }
            _ => {}
        }
    }
    if i1 > i0 {
        let (_, p) = packet_parser(&text[i0..i1])?;
        packets.push(p);
    }
    Ok(("", Packet::List(packets)))
}

pub fn packet_parser(text: &str) -> IResult<&str, Packet> {
    if let Ok((input, p)) = int_primary(text) {
        // It's an int so just return that
        return Ok((input, Packet::Int(p)));
    }
    // It  must be a list
    let mut chars = text.chars();
    assert!(chars.next().unwrap() == '[');
    let mut count = 1;
    let mut ndx = 0;
    while count > 0 {
        let c = chars.next();
        match c.unwrap() {
            '[' => count += 1,
            ']' => count -= 1,
            _ => {}
        }
        ndx += 1;
    }
    return csp_parser(&text[1..ndx]);
}

fn parse_packet(text: &str) -> Packet {
    if let Ok((_, p)) = packet_parser(text) {
        return p;
    }
    panic!("bad packet");
}

pub fn load_packet_pairs(text: &str) -> Vec<(Packet, Packet)> {
    let mut vec = Vec::new();
    for pairs in text.trim().split("\n\n") {
        vec.push(
            pairs
                .split("\n")
                .map(|x| parse_packet(x.trim()))
                .collect_tuple()
                .unwrap(),
        )
    }
    vec
}

pub fn find_decoder_key(pairs: &Vec<(Packet, Packet)>) -> usize {
    let mut packets = Vec::new();
    for (p1, p2) in pairs {
        packets.push(p1);
        packets.push(p2);
    }
    let d1 = parse_packet("[[2]]");
    let d2 = parse_packet("[[6]]");
    packets.push(&d1);
    packets.push(&d2);
    packets.sort_by(|a, b| Packet::cmp(a, b));
    let mut key = 1;
    for (i, p) in packets.iter().enumerate() {
        if *p == &d1 || *p == &d2 {
            key *= i + 1
        }
    }
    key

    // dividers = [Packet(x) for x in (, "[[6]]")]
}
// def find_decoder_key(pairs):
//     """
//     >>> pairs = load_packets_pairs("data/example.txt")
//     >>> find_decoder_key(pairs)
//     140
//     """
//     packets, dividers = _sort_packets(pairs)
//     indices = []
//     for i, p in enumerate(packets):
//         if p in dividers:
//             indices.append(i + 1)
//     (a, b) = indices
//     return a * b
