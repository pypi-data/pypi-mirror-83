extern crate bindgen;

use std::env;
use std::path::PathBuf;

fn main() {
    println!(
        "cargo:rustc-link-search=native={}",
        env::var("DARKNET_ROOT").unwrap()
    );
    println!("cargo:rustc-link-lib=static=darknet");

    let bindings = bindgen::Builder::default()
        .header(env::var("DARKNET_ROOT").unwrap() + "/include/darknet.h")
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
