#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use tauri::command;

#[command]
fn process_pdf() -> Result<String, String> {
    let bin_path = "/home/elielton/Documentos/Projetos-Web/Generate-Tags/src-tauri/src/bin/pdf_parser";

    println!("Current dir: {:?}", std::env::current_dir());

    let output = Command::new(bin_path)
        .arg("/home/elielton/Downloads/report.pdf")
        .output()
        .map_err(|e| e.to_string())?;

    if output.status.success() {
        let result = String::from_utf8_lossy(&output.stdout).to_string();
        Ok(result)
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![process_pdf])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
