#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use tauri::command;
use std::path::PathBuf;

fn get_bin_path() -> PathBuf {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));

    if cfg!(target_os = "windows") {
        path.push("utils/pdf_parser.exe"); // binário Windows
    } else {
        path.push("utils/pdf_parser");     // binário Linux/macOS
    }

    path
}

#[command]
fn process_pdf(file: String) -> Result<String, String> {
    let bin_path = get_bin_path();

    let output = Command::new(bin_path)
        .arg(file)
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
