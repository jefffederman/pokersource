<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE xsl:stylesheet [<!ENTITY nbsp "&#160;">]>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="/html[@lang='en']/body/div">
    <!-- Title bar -->
    <table width="100%" border="0" cellspacing="0" cellpadding="8">
      <tr>
	<td class="TopBody">
	  <a class="Logo" href="{$root}/index.en.html">
            PokerSource
	  </a>
	</td>
	<td align="right" valign="bottom" class="TopBody">
	  
	</td>
      </tr>
    </table>

    <table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
	<td width="99%" valign="top">
	  <div class="content">
	    <xsl:apply-templates select="@*|node()"/>
	  </div>
	</td>

	<!-- Menu column. On the right to be Lynx friendly.  -->
	<td>&nbsp;</td>
	<td valign="top" class="TopBody">
	  <table summary="" width="150" border="0" cellspacing="0" cellpadding="4">
	    <tr><td class="TopTitle" align="center">Development</td></tr>
	    <tr>
	      <td class="TopBody" align="right">
		<a class="TopBody" href="https://gna.org/files/?group=pokersource">Download</a><br />	          
		<a class="TopBody" href="https://gna.org/support/?group=pokersource">Bug report</a><br />
		<a class="TopBody" href="https://gna.org/cvs/?group=pokersource">CVS</a><br />
		<a class="TopBody" href="https://mail.gna.org/public/pokersource-users/">Mailing list</a><br />
	      </td>
	    </tr>
	    <tr><td class="TopTitle" align="center">Software</td></tr>
	    <tr>
	      <td class="TopBody" align="right">
		<a class="TopBody" href="{$root}/poker-eval.en.html">poker-eval</a><br />
		<a class="TopBody" href="{$root}/poker-engine.en.html">poker-engine</a><br />
		<a class="TopBody" href="{$root}/poker-network.en.html">poker-network</a><br />
	      </td>
	    </tr>
	    <tr><td class="TopTitle" align="center">Contact</td></tr>
	    <tr><td class="TopBody" align="center"><a href="mailto:loic@gnu.org">Loic Dachary</a></td></tr>
	  </table>
	</td>
      </tr>
    </table>

    <!-- Bottom line -->
    <table width="100%" border="0" cellspacing="0" cellpadding="2">
      <tr>
	<td class="newstext" align="center">
	  <font size="-2">
	    Copyright (C) 2006 Loic Dachary &lt;loic@gnu.org&gt;
	    <br/>
	    Verbatim copying and distribution of this entire article is
	    permitted in any medium, provided this notice is preserved.
	  </font>
	</td>
        <td class="newstext">&nbsp;</td>
      </tr>
    </table>
  </xsl:template> 

<!--
Local Variables: ***
mode: nxml ***
End: ***
-->
</xsl:stylesheet>
