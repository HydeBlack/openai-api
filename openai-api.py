import os
import pdfplumber
import json
import openai
import csv
from fpdf import FPDF

# Configure OpenAI API key
openai.api_key = "insert_you_key_here"

# Text extraction from PDF
def extract_text_from_pdf(pdf_path):
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_data.append(page.extract_text())
    if not text_data:
        raise ValueError("Não encontrei dados no arquivo PDF.")
        print("Pressione ENTER para continuar.")
        input("")
    return text_data

# Filter lines by charge codes
def filter_lines_by_codes(text_data, charge_codes):
    charge_codes = [code.strip() for code in charge_codes]
    filtered_lines = {code: [] for code in charge_codes}

    current_code = None
    buffer_line = ""

    for page in text_data:
        for line in page.splitlines():
            line = line.strip()
            if not line:
                continue

            for code in charge_codes:
                if line.startswith(code):
                    if current_code and buffer_line:
                        filtered_lines[current_code].append(buffer_line.strip())
                    current_code = code
                    buffer_line = line
                    break
            else:
                if current_code:
                    buffer_line += " " + line

    if current_code and buffer_line:
        filtered_lines[current_code].append(buffer_line.strip())

    return filtered_lines

# Save JSON
def save_json(data, pdf_name):
    output_path = f"{os.path.splitext(pdf_name)[0]}.json"
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return output_path

# Convert JSON to CSV
def convert_json_to_csv(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    csv_path = f"{os.path.splitext(json_path)[0]}.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Charge Code", "Details"])
        for code, details in data.items():
            for detail in details:
                filtered_detail = detail.replace(code, '').strip()
                writer.writerow([code, filtered_detail])
    return csv_path

# Convert JSON to PDF
def convert_json_to_pdf(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Parsed Data", ln=True, align='C')
    pdf.ln(10)

    for code, details in data.items():
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 10, txt=f"Charge Code: {code}", ln=True)
        pdf.set_font("Arial", size=12)
        for detail in details:
            pdf.multi_cell(0, 10, detail)
        pdf.ln(5)

    pdf_path = f"{os.path.splitext(json_path)[0]}-parsed.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Main parsing function
def parse_pdf():
    pdf_files = [f for f in os.listdir() if f.endswith('.pdf')]
    if not pdf_files:
        print("Não encontrei PDFs na pasta.")
        print("Pressione ENTER para continuar.")
        input("")
        return

    for pdf_path in pdf_files:
        print(f"Processando {pdf_path}...")
        try:
            text_data = extract_text_from_pdf(pdf_path)
            charge_codes = input("Insira os charge codes separados por vírgulas: ").split(',')
            filtered_lines = filter_lines_by_codes(text_data, charge_codes)
            json_path = save_json(filtered_lines, pdf_path)
            print(f"JSON salvo como {json_path}")
            print("Pressione ENTER para continuar.")
            input("")
        except Exception as e:
            print(f"Erro ao processar {pdf_path}: {e}")

# View JSON
def view_json():
    json_files = [f for f in os.listdir() if f.endswith('.json')]
    if not json_files:
        print("Não encontrei arquivos JSON na pasta.")
        print("Pressione ENTER para continuar.")
        input("")
        return

    for json_file in json_files:
        print(f"\nContents of {json_file}:")
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(json.dumps(data, indent=4, ensure_ascii=False))
            print("Pressione ENTER para continuar.")
            input("")

# Export JSON to CSV
def export_json_to_csv():
    json_files = [f for f in os.listdir() if f.endswith('.json')]
    if not json_files:
        print("Não encontrei arquivos JSON na pasta.")
        print("Pressione ENTER para continuar.")
        input("")
        return

    for json_file in json_files:
        csv_path = convert_json_to_csv(json_file)
        print(f"CSV salvo como {csv_path}")
        print("Pressione ENTER para continuar.")
        input("")

# Export JSON to PDF
def export_json_to_pdf():
    json_files = [f for f in os.listdir() if f.endswith('.json')]
    if not json_files:
        print("Não encontrei arquivos JSON na pasta.")
        print("Pressione ENTER para continuar.")
        input("")
        return

    for json_file in json_files:
        pdf_path = convert_json_to_pdf(json_file)
        print(f"PDF salvo como {pdf_path}")
        print("Pressione ENTER para continuar.")
        input("")

# Create menu
def criarMenu():
    os.system("cls")
    linha = "+" + "-" * 68 + "+"
    opcoes = [
        "| 1. Buscar PDFs na pasta e extrair dados para JSON                  |",
        "| 2. Exibir JSON na tela                                             |",
        "| 3. Exportar JSON para CSV                                          |",
        "| 4. Exportar JSON para PDF                                          |",
        "| 5. Sair                                                            |"
    ]
    print(linha)
    print("|                                                                    |")
    print("|               Programa de parsing de invoices em PDF               |")
    print("|                                                                    |")
    print("|                                                                    |")
    print("|2024-11-20 --- Versão 1.0 --- Eder Castro: design, pesquisa e código|")
    print("|                                                                    |")
    print(linha)
    for opcao in opcoes:
        print(opcao)
    print(linha)

# Main menu
def main():
    while True:
        criarMenu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            parse_pdf()
        elif opcao == '2':
            view_json()
        elif opcao == '3':
            export_json_to_csv()
        elif opcao == '4':
            export_json_to_pdf()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            input("Pressione ENTER para retornar ao menu.")

if __name__ == "__main__":
    main()
