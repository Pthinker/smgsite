<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes" encoding="utf8" media-type="text/html" />

<xsl:template match="/">
	<xsl:apply-templates select="catalog" />
</xsl:template>

<xsl:template match="catalog">	
	<xsl:apply-templates select="content/topic" />
</xsl:template>

<xsl:template match="topic">
	<xsl:apply-templates select="body" />
	<p class="library_topic_credits"><!-- Note: the attribution is required by the RelayHealth license --><xsl:value-of select="attribution" /><br />
	<!-- Note: the publisher is suggested by RelayHealth --><xsl:value-of select="publisher" /><br />
	<!-- Note: the copyright is required by the RelayHealth license --><xsl:value-of select="copyright" /></p>
</xsl:template>

<xsl:template match="body">
	<xsl:apply-templates />
</xsl:template>

<xsl:template match="header[@type='primary']">
	<p class="library_subhead_navy_blue_bold">
		<xsl:apply-templates />
	</p>
</xsl:template>

<xsl:template match="complexContent[@type='crsTable']">
	<pre>
		<xsl:apply-templates />
	</pre>
</xsl:template>

<xsl:template match="flag[@prespref='b']">
	<b><xsl:apply-templates /></b>
</xsl:template>

<xsl:template match="flag[@prespref='i']">
	<em><xsl:apply-templates /></em>
</xsl:template>

<xsl:template match="linkExternal">
	<a>
		<xsl:attribute name="href">
			<xsl:value-of select="@url"/>
		</xsl:attribute>
		<xsl:apply-templates />
	</a>
</xsl:template>

<xsl:template match="list[@style='bullet']">
	<ul class="orange_bullets">
		<xsl:apply-templates />
	</ul>
</xsl:template>

<xsl:template match="list[@style='letter']">
	<ol class="ol_letter_list">
		<xsl:apply-templates />
	</ol>
</xsl:template>

<xsl:template match="list[@style='number']">
	<ol class="ol_number_list">
		<xsl:apply-templates />
	</ol>
</xsl:template>

<xsl:template match="listitem">
	<li><xsl:apply-templates /></li>
</xsl:template>

<xsl:template match="p">
	<p><xsl:apply-templates /></p>
</xsl:template>

</xsl:stylesheet>