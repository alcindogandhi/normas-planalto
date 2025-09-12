<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title><xsl:value-of select="doc/info/titulo"/></title>
        <style>
          body { font-family: Arial, sans-serif; margin: 12pt; }
          h1 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 20pt; }
          h2 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 18pt; }
          h3 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 16pt; }
          h4 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 15pt; }
          h5 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 14pt; }
          h6 { margin-top: 1em; margin-bottom: 0; text-align: center; font-size: 13pt; }
          p.title { font-size: 22pt; }
          div.info p { text-align: center; font-size: 14pt; }
          div.parte p { text-align: center; font-size: 18pt;}
          div.livro p { text-align: center; font-size: 18pt;}
          div.titulo p { text-align: center; font-size: 16pt;}
          div.capitulo p { text-align: center; font-size: 15pt;}
          div.secao p { text-align: center; font-size: 14pt;}
          div.artigo p { text-align: justify; font-size: 12pt; margin-left: 10pt; }
          div.titulo div.texto p { text-align: justify; font-size: 12pt; font-weight: bold; margin-left: 10pt; }
          div.texto p { text-align: justify; font-size: 12pt; margin-left: 10pt; }
          div.artigo div.texto p { text-align: justify; font-size: 12pt; margin-left: 10pt; }
          .paragrafo, .inciso, .alinea, .texto { margin-left: 25pt; }
          .assinaturas { margin-top: 2em; }
        </style>
      </head>
      <body>
        <div class="info">
          <h1><xsl:value-of select="doc/info/titulo"/></h1>
          <p class="title"><xsl:value-of select="doc/info/tipo"/> Nº <xsl:value-of select="doc/info/numero"/>, DE <xsl:value-of select="doc/info/data"/></p>
          <p><xsl:value-of select="doc/info/descricao"/></p>
        </div>

        <div class="artigo">
          <p><xsl:value-of select="doc/preambulo"/></p>
        </div>

        <!-- Seção preliminar -->
        <xsl:apply-templates select="doc/Secao[@id='I']"/>

        <!-- Livros -->
        <xsl:apply-templates select="doc/Parte"/>
        <xsl:apply-templates select="doc/Livro"/>
        <xsl:apply-templates select="doc/Titulo"/>
        <xsl:apply-templates select="doc/Capitulo"/>

        <!-- Seção final -->
        <xsl:apply-templates select="doc/Secao[@id='F']"/>

        <!-- Artigos livres -->
        <xsl:apply-templates select="doc/Artigo"/>

        <!-- Assinaturas -->
        <div class="assinaturas">
          <xsl:for-each select="doc/info/assinaturas/nome">
            <p><xsl:value-of select="."/></p>
          </xsl:for-each>
        </div>
      </body>
    </html>
  </xsl:template>

  <!-- Secão -->
  <xsl:template match="Secao">
    <div class="secao">
      <h5><xsl:value-of select="@text"/></h5>
      <xsl:apply-templates select="Artigo"/>
    </div>
  </xsl:template>

  <!-- Parte -->
  <xsl:template match="Parte">
    <div class="parte">
      <h2>PARTE <xsl:value-of select="@text"/></h2>
      <xsl:apply-templates select="Livro|Titulo|Texto"/>
    </div>
  </xsl:template>

  <!-- Livro -->
  <xsl:template match="Livro">
    <div class="livro">
      <h2>LIVRO <xsl:value-of select="@id"/></h2>
      <p><xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Titulo|Texto"/>
    </div>
  </xsl:template>

  <!-- Título -->
  <xsl:template match="Titulo">
    <div class="titulo">
      <h3>TÍTULO <xsl:value-of select="@id"/></h3>
      <p><xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Capitulo|Artigo|Texto"/>
    </div>
  </xsl:template>

  <!-- Capítulo -->
  <xsl:template match="Capitulo">
    <div class="capitulo">
      <h4>CAPÍTULO <xsl:value-of select="@id"/></h4>
      <p><xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Secao|Artigo|Texto"/>
    </div>
  </xsl:template>

  <!-- Artigo -->
  <xsl:template match="Artigo">
    <div class="artigo">
      <p><strong>Art. <xsl:value-of select="@id"/>: </strong><xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Inciso|Paragrafo|Alinea|Texto"/>
    </div>
  </xsl:template>

  <!-- Inciso -->
  <xsl:template match="Inciso">
    <div class="inciso">
      <p><xsl:value-of select="@id"/> - <xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Alinea|Paragrafo|Texto"/>
    </div>
  </xsl:template>

  <!-- Parágrafo -->
  <xsl:template match="Paragrafo">
    <div class="paragrafo">
      <p>
        <xsl:choose>
          <xsl:when test="@id='U'">Parágrafo único: <xsl:value-of select="@text"/></xsl:when>
          <xsl:otherwise>§ <xsl:value-of select="@id"/>: <xsl:value-of select="@text"/></xsl:otherwise>
        </xsl:choose>
      </p>
      <xsl:apply-templates select="Inciso|Alinea|Texto"/>
    </div>
  </xsl:template>

  <!-- Alínea -->
  <xsl:template match="Alinea">
    <div class="alinea">
      <p><xsl:value-of select="@id"/> ) <xsl:value-of select="@text"/></p>
      <xsl:apply-templates select="Texto"/>
    </div>
  </xsl:template>

  <!-- Texto -->
  <xsl:template match="Texto">
    <div class="texto">
      <p><xsl:value-of select="."/></p>
    </div>
  </xsl:template>

</xsl:stylesheet>
