<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes" encoding="utf8" media-type="text/html" />

<xsl:template match="/">
	<div id="index_col_left_365">
		<p><span class="navy_blue_bold"><xsl:value-of select="catalog/title" /></span></p>
		<xsl:apply-templates select="catalog/content/index/body" />
		<p class="font_minus_1"><!-- Note: the copyright is required by the RelayHealth license --><xsl:value-of select="catalog/content/index/copyright" /></p>
	</div>
</xsl:template>

<xsl:template match="body">
	<div id="alphabet_nav_box">
		<p>
			<a style="margin-right:15px;" href="#letter-A">A</a>
			<a style="margin-right:15px;" href="#letter-B">B</a>
			<a style="margin-right:15px;" href="#letter-C">C</a>
			<a style="margin-right:15px;" href="#letter-D">D</a>
			<a style="margin-right:15px;" href="#letter-E">E</a>
			<a style="margin-right:15px;" href="#letter-F">F</a>
			<a style="margin-right:15px;" href="#letter-G">G</a>
			<a style="margin-right:15px;" href="#letter-H">H</a>
			<a style="margin-right:15px;" href="#letter-I">I</a>
			<a style="margin-right:15px;" href="#letter-J">J</a>
			<a style="margin-right:15px;" href="#letter-K">K</a>
			<a style="margin-right:15px;" href="#letter-L">L</a>
			<a style="margin-right:15px;" href="#letter-M">M</a>
			<a style="margin-right:15px;" href="#letter-N">N</a>
			<a style="margin-right:15px;" href="#letter-O">O</a>
			<a style="margin-right:15px;" href="#letter-P">P</a>
			<a style="margin-right:15px;" href="#letter-Q">Q</a>
			<a style="margin-right:15px;" href="#letter-R">R</a>
			<a style="margin-right:15px;" href="#letter-S">S</a>
			<a style="margin-right:15px;" href="#letter-T">T</a>
			<a style="margin-right:15px;" href="#letter-U">U</a>
			<a style="margin-right:15px;" href="#letter-V">V</a>
			<a style="margin-right:15px;" href="#letter-W">W</a>
			<a style="margin-right:15px;" href="#letter-X">X</a>
			<a style="margin-right:15px;" href="#letter-Y">Y</a>
			<a style="margin-right:15px;" href="#letter-Z">Z</a>
		</p>
	</div>
	<xsl:apply-templates select="section" />
</xsl:template>

<xsl:template match="section">
	<a>
		<xsl:attribute name="name">letter-<xsl:value-of select="substring(@name, 1, 1)" /></xsl:attribute>
		<div id="doctors_alpha_list_header"><span class="doctors_index_header">
			<xsl:value-of select="@name" />
		</span></div>
	</a>
	<div id="doctors_alpha_list_730_box">
	<ul class="doctors_alpha_index_left_ul">	
		<xsl:for-each select="entry[count(descendant::*/label) + count(following-sibling::*/descendant::label) &gt; (count(..//label) div 2)]">
			<xsl:apply-templates />
		</xsl:for-each>
	</ul>
	<ul class="doctors_alpha_index_right_ul">
		<xsl:for-each select="entry[count(descendant::*/label) + count(following-sibling::*/descendant::label) &lt;= (count(..//label) div 2)]">
			<xsl:apply-templates />
		</xsl:for-each>
	</ul>
	</div>		
</xsl:template>

<xsl:template match="entry">
	<xsl:apply-templates />
</xsl:template>

<xsl:template match="label">
	<xsl:if test="not(contains(., 'Illustrations')) and not(contains(.,'illustration')) and not(contains(.,'brief version'))">
		<li class="doctors_alpha_name_li">
			<xsl:choose>
				<xsl:when test="count(ancestor::*) &gt; 7">
					<xsl:attribute name="style">margin-left:30px;</xsl:attribute>
				</xsl:when>
				<xsl:when test="count(ancestor::*) &gt; 6">
					<xsl:attribute name="style">margin-left:15px;</xsl:attribute>
				</xsl:when>
			</xsl:choose>
			<xsl:apply-templates />
		</li>
	</xsl:if>
</xsl:template>

<xsl:template match="linkCRS">
	<a>
		<xsl:attribute name="href">/library/id/<xsl:value-of select="@id" />/</xsl:attribute>
		<xsl:apply-templates />
	</a>
</xsl:template>

<xsl:template match="text()">
	<xsl:choose>
		<xsl:when test="contains(.,'*')">
  			<xsl:value-of select="substring-before(.,'*')" />
		</xsl:when>
		<xsl:otherwise>
  			<xsl:value-of select="." />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

</xsl:stylesheet>
