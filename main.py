from pypdf import PdfReader, PdfWriter
import re

"--------------Principal----------------------"

escrever = PdfWriter()

leitura = PdfReader(r"/home/Aquivo.pdf")
numero_paginas = len(leitura.pages)

for x in range(7, 158): 
    pagina = leitura.pages[x]
    escrever.add_page(leitura.pages[x])


with open("novo.pdf", "wb") as f:
    escrever.write(f)



"--------------Segundaria (Feito p/ IA)----------------------"

# Caminho do PDF
caminho_pdf = "/home/novo.pdf"

leitura = PdfReader(caminho_pdf)

# Regex para detectar números romanos (linha isolada)
padrao_romano = re.compile(r'^\s*[IVXLCDM]{1,5}\s*$', re.MULTILINE)

inicio_capitulos = []

# 🔍 1. Detectar início dos capítulos
for i, pagina in enumerate(leitura.pages):
    texto = pagina.extract_text()

    if texto:
        linhas = texto.split("\n")

        for linha in linhas:
            if padrao_romano.match(linha.strip()):
                inicio_capitulos.append(i)
                break  # evita repetir a mesma página

print("Início dos capítulos:", inicio_capitulos)


# 🧩 2. Criar intervalos (inicio, fim)
capitulos = []

for i in range(len(inicio_capitulos)):
    inicio = inicio_capitulos[i]

    if i < len(inicio_capitulos) - 1:
        fim = inicio_capitulos[i + 1] - 1
    else:
        fim = len(leitura.pages) - 1

    capitulos.append((inicio, fim))

print("Capítulos (intervalos):", capitulos)


# 📦 3. Agrupar de 5 capítulos
grupos = [capitulos[i:i+5] for i in range(0, len(capitulos), 5)]


# 📄 4. Criar PDFs
for i, grupo in enumerate(grupos):
    writer = PdfWriter()

    for inicio, fim in grupo:
        for pagina in range(inicio, fim + 1):
            writer.add_page(leitura.pages[pagina])

    nome_arquivo = f"/home/novo_{i+1}.pdf"

    with open(nome_arquivo, "wb") as f:
        writer.write(f)

    print(f"PDF criado: {nome_arquivo}")