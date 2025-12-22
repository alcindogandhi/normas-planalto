#!/bin/sh

# Indo para a pasta do script
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH" || exit 1

# Verificando se o Python 3 está instalado
command -v python3 1>/dev/null 2>&1
if [ $? -ne "0" ]; then
    echo "Python 3 não está instalado. Por favor, instale o Python 3 para continuar."
    exit 1
fi

# Verificando se o Pandoc está instalado
command -v pandoc 1>/dev/null 2>&1
if [ $? -ne "0" ]; then
    echo "Pandoc não está instalado. Por favor, instale o Pandoc para continuar."
    exit 1
fi

# Verificando se o Xsltproc está instalado
command -v xsltproc 1>/dev/null 2>&1
if [ $? -ne "0" ]; then
    echo "Xsltproc não está instalado. Por favor, instale o Xsltproc para continuar."
    exit 1
fi

# Verificando se o ambiente virtual do Python está habilitado
if [ -z "$VIRTUAL_ENV" ]; then
    # Verificando se o ambiente virtual do Python está configurado
    if [ ! -d "venv" ]; then
        echo "Ambiente virtual do Python não encontrado. Criando um novo ambiente virtual..."
        python3 -m venv venv
    fi

    # Ativando o ambiente virtual
    # shellcheck source=/dev/null
    . venv/bin/activate

    # Instalando as dependências do Python
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Limpando e criando a pasta build
rm -fr build
mkdir build

# Executando o script principal em Python e o script de conversão para EPUB
echo
python3 src/main.py
if [ $? -ne 0 ]; then
    echo "O script principal falhou. Saindo..."
    exit 1
fi

sh src/xml_to_epub.sh
if [ $? -ne 0 ]; then
    echo "A conversão para EPUB falhou. Saindo..."
    exit 1
fi
