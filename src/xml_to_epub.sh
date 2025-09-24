#!/bin/sh

XSLT="../src/doc.xslt"
CAPA="../src/capa.svg"

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH/../build" || exit 1
mkdir -p ../html

echo
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
    DATA=$(grep "<data>" $XML | cut -d'>' -f2 | cut -d'<' -f1)
    DIA=$(echo $DATA | cut -d' ' -f1)
    MES=$(echo $DATA | cut -d' ' -f3)
    ANO=$(echo $DATA | cut -d' ' -f5)
    
    NAME="$TIPO Nº $NUMERO/$ANO"
    AUTHOR="BRASIL"

    sed "s|@name|$NAME|" $CAPA | sed "s|@title|$TITULO|" > $SVG
    if [ $? -ne 0 ]; then
        echo "Erro na geração da capa SVG"
        exit 1
    fi
    xsltproc $XSLT $XML > $HTML
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

	cp $HTML ../html/
	cp $EPUB ../epub/
done

