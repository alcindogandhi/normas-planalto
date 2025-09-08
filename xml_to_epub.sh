#!/bin/sh

XSLT=doc.xslt
CAPA=capa.svg

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH/build" || exit 1

for xml in *.xml; do
    echo "Processando o arquvo $xml ..."
    
    XML=$xml
    PREFIX=$(echo $XML | cut -d'.' -f1)
    HTML=${PREFIX}.html
    EPUB=${PREFIX}.epub
    SVG=${PREFIX}.svg

    TITULO=$(grep "<titulo>" $XML | cut -d'>' -f2 | cut -d'<' -f1)
    TIPO=$(grep "<tipo>" $XML | cut -d'>' -f2 | cut -d'<' -f1)
    NUMERO=$(grep "<numero>" $XML | cut -d'>' -f2 | cut -d'<' -f1 )
    ANO=$(grep "<data>" $XML | cut -d'>' -f2 | cut -d'<' -f1 | rev | cut -d' ' -f-1 | rev)

    NAME="$TIPO Nº $NUMERO/$ANO"
    AUTHOR="BRASIL"

    sed "s|@name|$NAME|" ../$CAPA | sed "s|@title|$TITULO|" > $SVG
    if [ $? -ne 0 ]; then
        echo "Erro na geração da capa SVG"
        exit 1
    fi
    xsltproc ../$XSLT $XML > $HTML
    if [ $? -ne 0 ]; then
        echo "Erro na transformação XSLT"
        exit 1
    fi
    pandoc $HTML -o $EPUB --metadata title="$TITULO" --metadata author="$AUTHOR" --epub-cover-image=$SVG
    if [ $? -ne 0 ]; then
        echo "Erro na conversão para EPUB"
        exit 1
    fi
    echo "Arquivo EPUB gerado: $EPUB"
    echo
done

