#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::command;
use std::process::Command;

#[command]
fn process_pdf(file_path: String) -> Result<String, String> {
    let bin_path = if cfg!(target_os = "windows") {
        "./src-tauri/bin/pdf_parser.exe"
    } else {
        "./src-tauri/bin/pdf_parser"
    };

    let output = Command::new(bin_path)
        .arg(file_path)
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
        .invoke_handler(tauri::generate_handler![process_pdf])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
