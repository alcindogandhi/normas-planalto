import re
import xml.etree.ElementTree as ET

# Expressões regulares para identificar seções
patterns = {
    "livro": re.compile(r"^LIVRO\s+([a-zA-Z]+)", re.IGNORECASE),
    "titulo": re.compile(r"^T[IÍ]TULO\s+(X{0,3}I{1,3}|X{0,3}IV|X{0,3}VI{0,3}|X{0,3}IX{1,3}|X{1,3})", re.IGNORECASE),
    "capitulo": re.compile(r"^CAP[IÍ]TULO\s+(X{0,3}I{1,3}|X{0,3}IV|X{0,3}VI{0,3}|X{0,3}IX{1,3}|X{1,3})", re.IGNORECASE),
    "secao": re.compile(r"^Se[cç][aã]o\s+(X{0,3}I{1,3}|X{0,3}IV|X{0,3}VI{0,3}|X{0,3}IX{1,3}|X{1,3})", re.IGNORECASE),
    "artigo": re.compile(r"^Art.\s*(\d+-?[A-Za-z]?)[Oo°ºª\.]?\s*[-]?\s*(.+)", re.IGNORECASE),
    "artigos": re.compile(r"^Arts.\s*(\d+\sa\s\d+)\s*\.?\s*(.*)", re.IGNORECASE),
    "paragrafo": re.compile(r"^§\s*(\d+)[o°ºª]\s*(.+)", re.IGNORECASE),
    "paragrafos": re.compile(r"§§?\s?(\d+[o°ºª]?\s*.?\s*\d+.?)\s*(.*)", re.IGNORECASE),
    "paragrafoUnico": re.compile(r"^(Par[aá]grafo [uú]nico)\.\s+(.+)", re.IGNORECASE),
    "inciso": re.compile(r"^(X{0,3}I{1,3}|X{0,3}IV|X{0,3}VI{0,3}|X{0,3}IX{1,3}|X{1,3})\s*[-–]\s*(.+)", re.IGNORECASE),
    "alinea": re.compile(r"^([a-zA-Z])\)\s*(.*)", re.IGNORECASE),
    "final": re.compile(r"([A-Za-záéíóú ]+),?\s*(\d{1,2}.+\d{4}).+Independ[eê]ncia.+República", re.IGNORECASE)
}

# Função auxiliar para adicionar elementos
def append_element(parent, tag, text, attrib=None):
    elem = ET.SubElement(parent, tag, attrib if attrib else {})
    elem.text = text.strip()
    return elem

def generate_xml(txtFile: str, xmlFile: str, title: str):
    # Carrega o arquivo CTN
    with open(txtFile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Cria o elemento raiz do XML
    root = ET.Element("doc")

    # Inicializa os elementos atuais
    info = current_livro = current_titulo = current_capitulo = current_secao \
        = current_artigo = current_paragrafo = current_inciso = current_element = root

    # Processa cada linha e constrói a estrutura XML
    ignore = False
    for i, line in enumerate(lines):
        if ignore:
            ignore = False
            continue
        line = line.strip()
        if not line or (i < 4):
            continue

        # Lei
        if (i == 4):
            info = append_element(root, "info", "")
            tokens = line.split()
            if len(tokens) >= 9:
                tipo = tokens[0]
                num = tokens[2].replace(".", "").replace(",", "")
                data = " ".join(tokens[4:9]).replace(".", "").replace(",", "")
                append_element(info, "titulo", title)
                append_element(info, "tipo", tipo)
                append_element(info, "numero", num)
                append_element(info, "data", data)
            continue

        if (i == 5):
            append_element(info, "descricao", line)
            continue;
        
        if line.upper().startswith("DISPOSIÇÃO PRELIMINAR"):
            text = line.strip()
            current_element = current_secao = append_element(root, "Secao", "", {"id": "I", "text": text})
            current_inciso = current_paragrafo = current_artigo = current_secao
            continue
        
        if (i == 6):
            append_element(root, "preambulo", line)
            continue;
        
        if line.startswith("Disposições Finais"):
            text = line.strip()
            current_element = current_secao = append_element(root, "Secao", "", {"id": "F", "text": text})
            current_inciso = current_paragrafo = current_artigo = current_secao
            continue

        match = patterns["final"].match(line)
        if match:
            local = match.group(1)
            append_element(info, "local", local)
            ii = i + 1
            assinaturas = append_element(info, "assinaturas", "")
            while not lines[ii].startswith("Este texto"):
                append_element(assinaturas, "nome", lines[ii].strip())
                ii = ii + 1
            break;

        matched = False
        for key, pattern in patterns.items():
            match = pattern.match(line)
            if match:
                matched = True
                if key == "livro":
                    id = match.group(1)
                    text = lines[i+1].strip()
                    current_element = current_livro = append_element(root, "Livro", "", {"id": id, "text": text})
                    current_inciso = current_paragrafo = current_artigo = current_secao = current_capitulo = current_secao = current_artigo = current_titulo = current_livro
                    ignore = True
                elif key == "titulo":
                    id = match.group(1)
                    text = lines[i+1].strip()
                    current_element = current_titulo = append_element(current_livro, "Titulo", "", {"id": id, "text": text})
                    current_inciso = current_paragrafo = current_artigo = current_secao = current_capitulo = current_secao = current_artigo = current_titulo
                    ignore = True
                elif key == "capitulo":
                    id = match.group(1)
                    text = lines[i+1].strip()
                    current_element = current_capitulo = append_element(current_titulo, "Capitulo", "", {"id": id, "text": text})
                    current_inciso = current_paragrafo = current_artigo = current_secao = current_capitulo
                    ignore = True
                elif key == "secao":
                    id = match.group(1)
                    text = lines[i+1].strip()
                    current_element = current_secao = append_element(current_capitulo, "Secao", "", {"id": id, "text": text})
                    current_inciso = current_paragrafo = current_artigo = current_secao
                    ignore = True
                elif key == "artigo":
                    artigo_id = match.group(1)
                    artigo_text = match.group(2)
                    current_element = current_artigo = append_element(current_secao, "Artigo", "", {"id": artigo_id, "text": artigo_text})
                    current_inciso = current_paragrafo = current_artigo
                elif key == "artigos":
                    artigo_id = match.group(1)
                    artigo_text = match.group(2)
                    current_element = current_artigo = append_element(current_secao, "Artigo", "", {"id": artigo_id, "text": artigo_text})
                    current_inciso = current_paragrafo = current_artigo
                elif key == "paragrafo":
                    par_id = match.group(1)
                    par_text = match.group(2)
                    current_element = current_paragrafo = append_element(current_artigo, "Paragrafo", "", {"id": par_id, "text": par_text})
                    current_inciso = current_paragrafo
                elif key == "paragrafos":
                    par_id = match.group(1)
                    par_text = match.group(2)
                    current_element = current_paragrafo = append_element(current_artigo, "Paragrafo", "", {"id": par_id, "text": par_text})
                    current_inciso = current_paragrafo
                elif key == "paragrafoUnico":
                    par_id = "U"
                    par_text = match.group(2)
                    current_element = current_paragrafo = append_element(current_artigo, "Paragrafo", "", {"id": par_id, "text": par_text})
                    current_inciso = current_paragrafo
                elif key == "inciso":
                    inciso_id = match.group(1)
                    inciso_text = match.group(2)
                    current_element = current_inciso = append_element(current_paragrafo, "Inciso", "", {"id": inciso_id, "text": inciso_text})
                elif key == "alinea":
                    alinea_id = match.group(1)
                    alinea_text = match.group(2)
                    current_element = append_element(current_inciso, "Alinea", "", {"id": alinea_id, "text": alinea_text})
                break

        if not matched:
            append_element(current_element, "Texto", line)

    # Salva o XML
    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(xmlFile, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    files = [
        {"txtFile": "build/ctn.txt", "title": "Código Tributário Nacional"},
        {"txtFile": "build/lindb.txt", "title": "Lei de Introdução às Normas do Direito Brasileiro"}
    ]
    for f in files:
        xmlFile = f["txtFile"].replace(".txt", ".xml")
        generate_xml(f["txtFile"], xmlFile, f["title"])
