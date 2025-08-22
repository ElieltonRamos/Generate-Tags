import json
import re
import csv
import pdfplumber

def ler_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            pagina_texto = pagina.extract_text() or ""
            texto += pagina_texto + "\n"
    return texto

def extract_products(text):
    products = []

    # Dados do pedido
    pedido_atual = {'tipo': '', 'numero': '', 'filial': '', 'data': '', 'endereco': ''}

    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    i = 0

    while i < len(lines):
        line = lines[i]

        # Cabeçalho de pedido (PV ou PTM)
        pedido_match = re.match(
            r'Tipo Pedido: (\w+) Pedido: (\d+) Filial Pedido: (\d+)(?: - .*?)? Dt\. Pedido(?: (\d{2}/\d{2}/\d{4}))?',
            line
        )
        if pedido_match:
            pedido_atual['tipo'] = pedido_match.group(1)
            pedido_atual['numero'] = pedido_match.group(2)
            pedido_atual['filial'] = pedido_match.group(3)
            pedido_atual['data'] = pedido_match.group(4) if pedido_match.group(4) else ''
            i += 1
            continue

        # Endereço de entrega
        if line.startswith('Endereço Entrega:'):
            pedido_atual['endereco'] = line.replace('Endereço Entrega:', '').strip()
            i += 1
            continue

        # Linha de dados de produto
        data_match = re.match(r'^(\d+)\s+(\S+)(?:\s+(\d{12,14}))?', line)
        if data_match:
            product = {
                'tipo_pedido': pedido_atual['tipo'],
                'numero_pedido': pedido_atual['numero'],
                'filial_pedido': pedido_atual['filial'],
                'data_pedido': pedido_atual['data'],
                'endereco_entrega': pedido_atual['endereco'],
                'description': '',
                'code': data_match.group(1),
                'supplier_code': data_match.group(2),
                'ean': data_match.group(3) if data_match.group(3) else '',
                'weight': '',
                'volume': '',
                'quantity': '',
                'vol_ace': '',
                'specifications': ''
            }

            parts = line.split()
            # Peso e volume
            numeros = [p for p in parts if re.match(r'^\d+,\d+$', p)]
            if numeros:
                product['weight'] = numeros[0]
                if len(numeros) > 1:
                    product['volume'] = numeros[1]
            # Quantidade e Vol/Ace
            if len(parts) >= 2 and re.match(r'^\d+$', parts[-2]):
                product['quantity'] = parts[-2]
            if len(parts) >= 1 and re.match(r'^\d+/\d+$', parts[-1]):
                product['vol_ace'] = parts[-1]

            # Descrição (linha anterior se não for cabeçalho ou endereço)
            if i > 0 and not lines[i-1].startswith(('Tipo Pedido:', 'Endereço Entrega:')):
                product['description'] = lines[i-1]

            # Especificações (linhas seguintes até próximo pedido ou linha de produto)
            specs = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith(('Tipo Pedido:', 'Endereço Entrega:', 'TOTAL')) \
                  and not re.match(r'^\d+\s+\S+', lines[j]):
                specs.append(lines[j])
                j += 1
            product['specifications'] = ' '.join(specs)

            products.append(product)
            i = j
            continue

        i += 1

    return products

# def save_products_csv(products, filename='products_list.csv'):
#     fieldnames = [
#         'tipo_pedido', 'numero_pedido', 'filial_pedido', 'data_pedido', 'endereco_entrega',
#         'description', 'code', 'supplier_code', 'ean', 'weight', 'volume', 'quantity', 'vol_ace', 'specifications'
#     ]
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(products)

def save_products_json(products, filename='products_list.json'):
    """
    Salva a lista de produtos em um arquivo JSON.
    Args:
        products (list): Lista de produtos.
        filename (str): Nome do arquivo JSON.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

# Exemplo de uso
if __name__ == '__main__':
    caminho_pdf = './report_multi-products.pdf'
    texto = ler_pdf(caminho_pdf)
    produtos = extract_products(texto)
    save_products_json(produtos)
    for produto in produtos:
        print(produto)
