use warp::{self, path, Filter};

fn main() {
    // GET /bla => 200 OK with body "Hello, bla!"
    let hello = path!(String)
        .map(|name| format!("Hello, {}!", name));

    let port = 8080;
    println!("Running server on port {}", port);
    warp::serve(hello)
        .run(([127, 0, 0, 1], port));
}
