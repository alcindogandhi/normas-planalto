import html_to_txt
import txt_to_xml
import os

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)

    files = [
        #{"url": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm", "txtFile": "build/cf88.txt", "title": "Constituição Federal", "cf": True, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm", "txtFile": "build/ctn.txt", "title": "Código Tributário Nacional", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm", "txtFile": "build/lindb.txt", "title": "Lei de Introdução às Normas do Direito Brasileiro", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm", "txtFile": "build/ccivil.txt", "title": "Código Civil", "cf": False, "discard": ["^Lei de Introdu.+"]},
        {"url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm", "txtFile": "build/cpcivil.txt", "title": "Código de Processo Civil", "cf": False, "discard": ["^Lei de Introdu.+"]},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/L8934compilado.htm", "txtFile": "build/cempr.txt", "title": "Código Empresarial", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3914.htm", "txtFile": "build/licp.txt", "title": "Lei de Introdução do Código Penal", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm", "txtFile": "build/cpenal.txt", "title": "Código Penal", "cf": False, "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm", "txtFile": "build/cppenal.txt", "title": "Código de Processo Penal", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm", "txtFile": "build/cdc.txt", "title": "Código de Defesa do Consumidor", "cf": False, "discard": []},
		#{"url": "https://www.planalto.gov.br/ccivil_03/leis/l9503compilado.htm", "txtFile": "build/ctb.txt", "title": "Código de Trânsito Brasileiro", "cf": False, "discard": []},
		#{"url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm", "txtFile": "build/nllc.txt", "title": "Nova Lei de Licitações e Contratos", "cf": False, "discard": []},
        #{"url": "https://raw.githubusercontent.com/alcindogandhi/normas-planalto/refs/heads/main/src/L14133.html", "txtFile": "build/nllc.txt", "title": "Nova Lei de Licitações e Contratos", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp24.htm", "txtFile": "build/lc24-1975.txt", "title": "Lei Complementar 24 de 1975", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm", "txtFile": "build/lc214-2025.txt", "title": "Lei Complementar 214 de 2025", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp87.htm", "txtFile": "build/lc87-1996.txt", "title": "Lei Complementar 87 de 1996 - Lei Kandir", "cf": False, "discard": []},
        #{"url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm", "txtFile": "build/lc123-2006.txt", "title": "Lei Complementar 123 de 2006 - Simples Nacional", "cf": False, "discard": []},
    ]
    for f in files:
        html_to_txt.html_to_text(f["url"], f["txtFile"], f["discard"])
        xmlFile = f["txtFile"].replace(".txt", ".xml")
        txt_to_xml.generate_xml(f["txtFile"], xmlFile, f["title"], f["cf"])
