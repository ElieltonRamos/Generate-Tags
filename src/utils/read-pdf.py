import re
import pdfplumber
import json
import os
import sys

# -------- Regex / Helpers --------
pedido_re = re.compile(
    r'Tipo Pedido:\s*(\w+)\s+Pedido:\s*(\d+)\s+Filial Pedido:\s*([^-\n\r]+?)(?:\s*-\s*(.*?))?(?:\s+Dt\. Pedido\s*(\d{2}/\d{2}/\d{4}))?$'
)

produto_dados_re = re.compile(r'^\d+\s+\S+.*\b\d+\s+\d+/\d+$')

def ler_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            pagina_texto = pagina.extract_text() or ""
            texto += pagina_texto + "\n"
    return texto

def clean_line_for_address(line):
    return re.sub(r'(?i)End[eê]re[cç]o Entrega:\s*', '', line).strip()

def normalize_whitespace(s):
    return re.sub(r'\s{2,}', ' ', s).strip()

# -------- Extração --------
def extract_all_products(texto):
    lines = [l.rstrip() for l in texto.splitlines()]
    stripped_lines = [l for l in lines if l.strip()]

    # localizar cabeçalhos de pedido
    headers = []
    for idx, line in enumerate(stripped_lines):
        m = pedido_re.match(line)
        if m:
            headers.append((idx, {
                'tipo_pedido': m.group(1) or '',
                'numero_pedido': m.group(2) or '',
                'filial_pedido': ((m.group(3) or '').strip() + ((' - ' + (m.group(4) or '').strip()) if m.group(4) else '')).strip(),
                'data_pedido': m.group(5) or ''
            }))

    if not headers:
        return []

    header_positions = [h[0] for h in headers] + [len(stripped_lines)]
    produtos = []

    for i, (hdr_idx, hdr_info) in enumerate(headers):
        start = hdr_idx
        end = header_positions[i+1]

        # procura linhas de especificacao
        spec_indices = [k for k in range(start, end) if produto_dados_re.match(stripped_lines[k])]

        # endereço
        endereco_lines = []
        if spec_indices:
            first_spec = spec_indices[0]
            addr_start = start + 1
            addr_end = first_spec - 2
            if addr_end >= addr_start:
                endereco_lines = stripped_lines[addr_start:addr_end+1]
            else:
                candidate_idx = start + 1
                if candidate_idx < end and (
                    'CEP' in stripped_lines[candidate_idx] or
                    'Endereço Entrega' in stripped_lines[candidate_idx] or
                    re.search(r'\d{5}-\d{3}', stripped_lines[candidate_idx])
                ):
                    endereco_lines = [stripped_lines[candidate_idx]]
        else:
            candidate_start = start + 1
            if candidate_start < end:
                endereco_lines = stripped_lines[candidate_start:end]

        endereco_original = "\n".join(endereco_lines).strip()
        endereco_normalizado = " ".join([clean_line_for_address(l) for l in endereco_lines if l.strip()])
        endereco_normalizado = normalize_whitespace(endereco_normalizado)

        # produtos do pedido
        for s in spec_indices:
            if s - 1 < start or s + 1 >= end:
                continue
            nome = stripped_lines[s-1].strip()
            especificacoes_line = stripped_lines[s].strip()
            descricao = stripped_lines[s+1].strip()

            if nome.startswith(('Endereço Entrega:', 'Tipo Pedido:', 'Separacao:')):
                continue

            tokens = especificacoes_line.split()
            code = tokens[0] if len(tokens) > 0 else ''
            supplier_code = tokens[1] if len(tokens) > 1 else ''
            ean = ''
            for t in tokens[2:]:
                if re.fullmatch(r'\d{12,14}', t):
                    ean = t
                    break
            quantity = ''
            for t in reversed(tokens):
                if re.fullmatch(r'\d+', t):
                    quantity = t
                    break
            vol_ace = ''
            for t in tokens:
                if re.fullmatch(r'\d+/\d+', t):
                    vol_ace = t
                    break

            produtos.append({
                'tipo_pedido': hdr_info['tipo_pedido'],
                'numero_pedido': hdr_info['numero_pedido'],
                'filial_pedido': hdr_info['filial_pedido'],
                'data_pedido': hdr_info['data_pedido'],
                'endereco_entrega': endereco_normalizado,
                'endereco_entrega_original': endereco_original,
                'nome': nome,
                'especificacoes': especificacoes_line,
                'descricao': descricao,
                'code': code,
                'supplier_code': supplier_code,
                'ean': ean,
                'quantity': quantity,
                'vol_ace': vol_ace
            })

    return produtos

# # -------- Main --------
# if __name__ == '__main__':
#     caminho_pdf = "./pdf/report6.pdf"
#     saida_json = "./produtos.json"
#
#     if not os.path.exists(caminho_pdf):
#         print(f"Arquivo não encontrado: {caminho_pdf}")
#         raise SystemExit(1)
#
#     texto = ler_pdf(caminho_pdf)
#     produtos = extract_all_products(texto)
#
#     with open(saida_json, "w", encoding="utf-8") as f:
#         json.dump(produtos, f, ensure_ascii=False, indent=2)
#
#     print(f"✅ Extraídos {len(produtos)} produtos")
#     print(f"Arquivo salvo em: {saida_json}")

# -------- Main --------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"status":"error","message":"Caminho do PDF não fornecido"}))
        sys.exit(1)

    caminho_pdf = sys.argv[1]

    if not os.path.exists(caminho_pdf):
        print(json.dumps({"status":"error","message":f"Arquivo não encontrado: {caminho_pdf}"}))
        sys.exit(1)

    texto = ler_pdf(caminho_pdf)

    # verificar se é PDF válido
    if "Relatorio Previa de Carregamento" not in texto:
        print(json.dumps({"status":"error","message":"PDF inválido: não contém 'Relatorio Previa de Carregamento'"}))
        sys.exit(1)

    produtos = extract_all_products(texto)

    print(json.dumps({"status":"ok","produtos":produtos}, ensure_ascii=False))