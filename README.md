# 📝 Generate Tags - Sistema de Leitura de PDFs 📄

Bem-vindo ao repositório do projeto **Generate Tags**!  
Este software faz a leitura de relatórios em **PDF 📑** e gera **etiquetas 🏷️** para conferência de mercadorias.  

⚠️ Importante: O **Generate Tags** foi desenvolvido especialmente para a empresa **Rede Norte de Espinosa** e funciona apenas com PDFs específicos utilizados nos seus relatórios internos.  

---

## 📑 Índice

- [🚀 Tecnologias Usadas](#-tecnologias-usadas)
- [💻 Ambiente de Desenvolvimento](#-ambiente-de-desenvolvimento)
- [⚙️ Instalação](#-instalação)
- [📞 Contato](#-contato)
- [📄 Licença](#-licença-para-uso)

---

## 🚀 Tecnologias Usadas

- [Node.js](https://nodejs.org/en/docs)
- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vue.js](https://vuejs.org/)
- [Tauri](https://tauri.app/)
- [Rust](https://www.rust-lang.org/)
- [Python](https://www.python.org/)

---

## 💻 Ambiente de Desenvolvimento

Este projeto foi desenvolvido utilizando **[Tauri](https://tauri.app/)** e **[Vue.js](https://vuejs.org/)**.  
Você pode executá-lo em modo de desenvolvimento ou gerar a instalação final para sua máquina.

---

### 🔹 Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

- [Node.js](https://nodejs.org/en/download/package-manager) (versão LTS recomendada)  
- [Rust](https://www.rust-lang.org/tools/install) (necessário para o Tauri)  
- [Tauri CLI](https://tauri.app/v1/guides/getting-started/prerequisites)  

> ⚠️ No Linux, pode ser necessário instalar pacotes adicionais como `libgtk-3-dev`, `libwebkit2gtk-4.1-dev`, entre outros. Veja a [documentação oficial](https://tauri.app/v1/guides/getting-started/prerequisites#setting-up-linux) para detalhes.

---

# Configuração de impressão (Elgin L42Pro, etiqueta 100 × 50 mm)

O app imprime etiquetas de **100 × 50 mm** (`@page { size: 100mm 50mm; margin: 0 }`). A impressora precisa ter um papel com essa mesma medida e o sensor calibrado.

## Requisitos

- Impressora Elgin L42Pro com driver instalado (Windows)
- Rolo de etiquetas 100 × 50 mm pré-moldadas (com espaço/gap entre etiquetas)

## 1. Criar o papel de etiquetas no driver

1. Painel de Controle → Dispositivos e Impressoras → botão direito em **ELGIN L42Pro** → **Preferências de impressão**.
2. Aba **Configuração de página** → em "Papel de etiquetas", clique em **Novo...**.
3. Preencha:

| Campo | Valor |
|---|---|
| Nome | `Etiqueta 100x50` |
| Tipo | Etiquetas cortadas com molde |
| Largura | `100.0 mm` |
| Altura | `50.0 mm` |
| Cartela exposta (Esquerda/Direita) | `0.0 mm` se o liner tem a mesma largura da etiqueta; se sobra papel nas laterais, usar a sobra medida de cada lado |

4. **OK**, selecione `Etiqueta 100x50` no campo Nome, **Aplicar** e **OK**.
5. Orientação: **Retrato**. Se a impressão sair rotacionada, trocar para **Paisagem**.

## 2. Calibrar o sensor de etiquetas

Sempre que criar/trocar o papel ou trocar o rolo:

1. Com as etiquetas instaladas, ligue a impressora e aguarde inicializar (somente o LED verde aceso).
2. Mantenha o botão **FEED** pressionado até o LED verde piscar **2 vezes** e solte.
3. Algumas etiquetas avançam sozinhas para a impressora reconhecer a altura.

Piscadas do FEED (manual L42Pro): 1 = auto teste (imprime configurações), 2 = calibração.

## 3. Diálogo de impressão do app

- Impressora: **ELGIN L42Pro**
- Margens: **Nenhuma**
- Escala: **100%**

## 4. Teste

Imprima **uma** etiqueta. Se o conteúdo sair alinhado dentro dela, está correto.

## Problemas comuns

| Sintoma | Causa provável | Ação |
|---|---|---|
| Conteúdo deslocado (cabeçalho em uma etiqueta, resto na seguinte) | Sensor não calibrado para o papel | Refazer a calibração (item 2) |
| Deslocamento aumenta a cada etiqueta | Medida do papel diferente da etiqueta física | Medir a etiqueta com régua e corrigir largura/altura no papel criado |
| Deslocamento vertical | Margem ou escala errada no diálogo | Margens "Nenhuma" e escala 100% |
| Saída rotacionada | Orientação | Alternar Retrato/Paisagem |

### 🔹 Rodando em modo de desenvolvimento

Após clonar o repositório, instale as dependências e inicie o projeto:

```bash📄
## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone git@github.com:ElieltonRamos/Generate-Tags.git
cd Generate-Tags

# Instalar dependências
npm install

# Rodar em modo de desenvolvimento
npm run tauri dev
```


## 🪛 Instaladores (Windows & Linux)

Na pasta **`Installer/`**, você encontrará os arquivos necessários para instalar o aplicativo com facilidade:

- 🐧 **Linux (Debian/Ubuntu):**  
  `Gerador-Etiquetas_0.1.0_amd64.deb` – Instalador do app para distribuições Linux baseadas em Debian/Ubuntu.  

- 🪟 **Windows (x64):**  
  `Gerador-Etiquetas_0.1.0_amd64.exe` – Instalador do app para Windows 64 bits.  

- 🐍 **Parser PDF (Executáveis em Python):**  
  Pasta `parser_pdf/` – Contém os binários responsáveis pela leitura e interpretação dos arquivos PDF.  

---

### ⚠️ Observação Importante

Após instalar o aplicativo, é necessário criar manualmente uma pasta chamada **`utils/`** no diretório onde o app foi instalado.  
Dentro dessa pasta, adicione o binário de leitura de PDF para que o sistema funcione corretamente.  

---

## Contato

Elielton Ramos

[![e-mail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:elieltonramos14@gmail.com)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/elielton-ramos/)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](elielton6554)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/elieltonramos08/)

---

## Licensa para uso

Open Source

Este projeto é de código aberto e está disponível para a comunidade. Sinta-se à vontade para explorar, clonar e contribuir com o projeto.

---

## Agradecimentos

Agradeço por todas as horas dedicadas, desafios superados e lições aprendidas durante o desenvolvimento deste projeto. Cada linha de código escrita foi um passo em direção ao meu crescimento como desenvolvedor e ao sucesso desta empreitada.

Gostaria também de expressar minha gratidão a todos os recursos educacionais, documentação e comunidades online que forneceram orientação, inspiração e suporte durante todo este processo.