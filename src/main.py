import html_to_txt
import txt_to_xml
import os

def create_index(itens: list[str]):
    with open("src/index.tpl", "r", encoding="utf-8") as f:
        template = f.read()
    list_html = "\n".join(itens)
    index_html = template.replace("<!--@list-->", list_html)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)

    files = [
        {"url": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm", "txtFile": "build/cf88.txt", "title": "Constituição Federal", "cf": True, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm", "txtFile": "build/ctn.txt", "title": "Código Tributário Nacional", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm", "txtFile": "build/lindb.txt", "title": "Lei de Introdução às Normas do Direito Brasileiro", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm", "txtFile": "build/ccivil.txt", "title": "Código Civil", "cf": False, "anexos": False, "discard": ["^Lei de Introdu.+"]},
        {"url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm", "txtFile": "build/cpcivil.txt", "title": "Código de Processo Civil", "cf": False, "anexos": False, "discard": ["^Lei de Introdu.+"]},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/L8934compilado.htm", "txtFile": "build/cempr.txt", "title": "Código Empresarial", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3914.htm", "txtFile": "build/licp.txt", "title": "Lei de Introdução do Código Penal", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm", "txtFile": "build/cpenal.txt", "title": "Código Penal", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm", "txtFile": "build/cppenal.txt", "title": "Código de Processo Penal", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm", "txtFile": "build/cdc.txt", "title": "Código de Defesa do Consumidor", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/l9503compilado.htm", "txtFile": "build/ctb.txt", "title": "Código de Trânsito Brasileiro", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm", "txtFile": "build/nllc.txt", "title": "Nova Lei de Licitações e Contratos", "cf": False, "anexos": False, "discard": []},
        {"url": "https://raw.githubusercontent.com/alcindogandhi/normas-planalto/refs/heads/main/src/L14133.html", "txtFile": "build/nllc.txt", "title": "Nova Lei de Licitações e Contratos", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp24.htm", "txtFile": "build/lc24-1975.txt", "title": "Lei Complementar 24 de 1975 - Convênios ICMS", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp87.htm", "txtFile": "build/lc87-1996.txt", "title": "Lei Complementar 87 de 1996 - Lei Kandir", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp105.htm", "txtFile": "build/lc105-2001.txt", "title": "Lei Complementar 105 de 2001 - Sigilo Bancário", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm", "txtFile": "build/lc116-2001.txt", "title": "Lei Complementar 116 de 2003 - ISS", "cf": False, "anexos": True, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm", "txtFile": "build/lc123-2006.txt", "title": "Lei Complementar 123 de 2006 - Simples Nacional", "cf": False, "anexos": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm", "txtFile": "build/lc214-2025.txt", "title": "Lei Complementar 214 de 2025 - IBS/CBS", "cf": False, "anexos": False, "discard": []},
    ]
    itens = []
    for f in files:
        html_to_txt.html_to_text(f["url"], f["txtFile"], f["anexos"], f["discard"])
        xmlFile = f["txtFile"].replace(".txt", ".xml")
        txt_to_xml.generate_xml(f["txtFile"], xmlFile, f["title"], f["cf"])
        htmlFile = f['txtFile'].replace(".txt", ".html").replace("build/", "html/")
        epubFile = f['txtFile'].replace(".txt", ".epub").replace("build/", "epub/")
        itens.append(f'<li><a class="norma-link" href="{htmlFile}">{f["title"]}</a><a class="epub-link" href="{epubFile}" title="Download EPUB"><img src="img/epub.svg" alt="Download EPUB" /></a></li>')
    
    create_index(itens)    
