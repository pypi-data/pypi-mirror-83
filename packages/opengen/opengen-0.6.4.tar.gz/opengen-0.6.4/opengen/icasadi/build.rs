use cc;
use std::path::Path;

fn main() {
    // Sanity checks to get better error messages

    // Check for F1
    assert!(
        Path::new("extern/auto_casadi_mapping_f1.c").exists(),
        "extern/auto_casadi_mapping_f1.c is missing"
    );

    // Check for F2
    assert!(
        Path::new("extern/auto_casadi_mapping_f2.c").exists(),
        "extern/auto_casadi_mapping_f2.c is missing"
    );

    // Check for Cost
    assert!(
        Path::new("extern/auto_casadi_cost.c").exists(),
        "extern/auto_casadi_cost.c is missing"
    );

    // Check for Grad
    assert!(
        Path::new("extern/auto_casadi_grad.c").exists(),
        "extern/auto_casadi_grad.c is missing"
    );

    // Check for Memory Allocator
    assert!(
        Path::new("extern/interface.c").exists(),
        "extern/interface.c is missing"
    );

    cc::Build::new()
        .flag_if_supported("-Wall")
        .flag_if_supported("-Wpedantic")
        .flag_if_supported("-Wno-long-long")
        .flag_if_supported("-Wno-unused-parameter")
        .pic(true)
        .include("src")
        .file("extern/auto_casadi_cost.c")
        .file("extern/auto_casadi_grad.c")
        .file("extern/auto_casadi_mapping_f2.c")
        .file("extern/auto_casadi_mapping_f1.c")
        .file("extern/interface.c")
        .compile("icasadi");

    // Rerun if these autogenerated files change
    println!("cargo:rerun-if-changed=extern/auto_casadi_cost.c");
    println!("cargo:rerun-if-changed=extern/auto_casadi_grad.c");
    println!("cargo:rerun-if-changed=extern/auto_casadi_mapping_f2.c");
    println!("cargo:rerun-if-changed=extern/auto_casadi_mapping_f1.c");
    println!("cargo:rerun-if-changed=extern/interface.c");
}
