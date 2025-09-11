from lxml import etree

def generate_html(xmlFile: str):
    xslFile = "doc.xslt"
    htmlFile = xmlFile.replace(".xml", ".html")

    xml = etree.parse(xmlFile)
    xslt = etree.parse(xslFile)
    transform = etree.XSLT(xslt)
    html = transform(xml)

    doc = xml.getroot()
    info = doc.find("info")
    titulo = info.find("titulo").text
    tipo = info.find("tipo").text
    numero = info.find("numero").text
    data = info.find("data")
    ano = data.text.split()[-1]
    
    nome = f"{tipo} nº {numero}/{ano}"

    with open(htmlFile, "wb") as file:
        file.write(etree.tostring(html, pretty_print=True, encoding="utf-8"))

    generate_svg(xmlFile, nome, titulo)

def generate_svg(xmlFile: str, nome: str, titulo: str):
    capa = "capa.svg"
    svgFile = xmlFile.replace(".xml", ".svg")
    with open(svgFile, "w", encoding='utf-8') as svg:
        with open(capa, "r", encoding='utf-8') as capaFile:
            for line in capaFile:
                svg.write(line.replace("@name", nome).replace("@title", titulo))

if __name__ == "__main__":
    xmlFile = "build/ctn.xml"
    generate_html(xmlFile)
