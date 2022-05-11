use std::cmp::Ordering;
use std::io;


fn main() {
    loop {
        println!("Put a word in!");
        let mut word = String::new();
        io::stdin().read_line(&mut word).expect("Put a word in!");
        let word = word.trim();

        let word_to_compare = "kaczka";
        let outcome = match word_to_compare.cmp(&word) {
            Ordering::Less => {
                println!("smaller!");
                "smaller"
            },
            Ordering::Equal => {
                println!("equal! Exiting!");
                return;
            },
            Ordering::Greater => {
                println!("greater!");
                "greater"
            },
        };
        println!("{} is {} than {}\n", word_to_compare, outcome, word);
    }
}
