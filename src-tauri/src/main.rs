#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::path::PathBuf;
use log::{info, debug, warn, error};
use simplelog::*;
use std::fs::File;
use tauri::command;

fn get_bin_path() -> PathBuf {
    // Pega o caminho do executável em runtime
    let mut path = std::env::current_exe().expect("❌ Não conseguiu pegar o caminho do executável");
    info!("📌 Caminho do executável: {:?}", path);

    // Remove o próprio exe, mantendo o diretório do app
    path.pop();
    info!("📂 Diretório do app: {:?}", path);

    // Adiciona a pasta utils
    path.push("utils");

    // Escolhe o binário dependendo do OS
    if cfg!(target_os = "windows") {
        path.push("pdf_parser_win10.exe");
    } else {
        path.push("pdf_parser_linux"); // sem .exe no Linux
    }

    info!("🔍 Caminho final do binário: {:?}", path);
    path
}


#[command]
fn process_pdf(file: String) -> Result<String, String> {
    let bin_path = get_bin_path();
    info!("📄 Processando PDF: {}", file);

    let output = Command::new(&bin_path)
        .arg(&file)
        .output()
        .map_err(|e| {
            error!("❌ Erro ao executar binário: {}", e);
            e.to_string()
        })?;

    if output.status.success() {
        let result = String::from_utf8_lossy(&output.stdout).to_string();
        debug!("✅ Saída do binário: {}", result);
        Ok(result)
    } else {
        let err = String::from_utf8_lossy(&output.stderr).to_string();
        error!("❌ Erro do binário: {}", err);
        Err(err)
    }
}

fn main() {
    // 🔹 Inicializa log em arquivo
    let log_path = if cfg!(target_os = "windows") {
        "C:\\gerador-etiquetas\\log.txt"
    } else {
        "log.txt"
    };

    CombinedLogger::init(vec![
        WriteLogger::new(
            LevelFilter::Debug, // log de Debug até Error
            Config::default(),
            File::create(log_path).expect("Não conseguiu criar log.txt"),
        ),
    ]).unwrap();

    info!("🚀 Aplicação iniciada");

    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![process_pdf])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
