import html_to_txt
import txt_to_xml
import os

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)

    files = [
        #{"url": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm", "txtFile": "build/cf88.txt", "title": "Constituição Federal", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm", "txtFile": "build/ctn.txt", "title": "Código Tributário Nacional", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm", "txtFile": "build/lindb.txt", "title": "Lei de Introdução às Normas do Direito Brasileiro", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm", "txtFile": "build/ccivil.txt", "title": "Código Civil", "discard": ["Lei de Introdu"]},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/L8934compilado.htm", "txtFile": "build/cempr.txt", "title": "Código Empresarial", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm", "txtFile": "build/cpenal.txt", "title": "Código Penal", "discard": []},
    ]
    for f in files:
        html_to_txt.html_to_text(f["url"], f["txtFile"], f["discard"])
        xmlFile = f["txtFile"].replace(".txt", ".xml")
        txt_to_xml.generate_xml(f["txtFile"], xmlFile, f["title"])
