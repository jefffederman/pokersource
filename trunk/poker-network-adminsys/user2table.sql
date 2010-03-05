DROP TABLE IF EXISTS `user2table`;
CREATE TABLE `user2table` (
  `user_serial` int(10) unsigned NOT NULL,
  `table_serial` int(10) unsigned NOT NULL,
  `money` int(11) NOT NULL default '0',
  `bet` int(11) NOT NULL default '0',
  PRIMARY KEY  (`user_serial`,`table_serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user2table` VALUES (4189668,282247,14300,0),(6764644,283207,155000,0),(9615956,282247,1475,0),(11995842,288115,2107500,0),(12510597,286729,10000,0),(12510597,288049,669000,128000),(12947486,282231,1645,10),(14825326,286729,967000,0),(15315047,288165,217000,4000),(16039386,285837,69000,0),(16728744,285837,1485000,0),(16960127,283203,130000,0),(17192528,288161,788000,2000),(17691837,286725,75000,0),(18333171,283203,59000,0),(18459261,282221,630,10),(18459261,282227,0,0),(20959831,282231,555,5),(24910663,285845,910000,0),(25060549,282241,0,1000),(25129493,283203,725000,0),(25129493,288161,195000,1000),(25396538,288125,349500,150000),(25710118,283935,3998000,0),(25781218,282231,1200,10),(26127323,282273,990,10),(26214075,282231,990,10),(26361507,282235,500,0),(26547012,285845,121000,0),(26547381,285837,111000,0),(27779553,288169,193000,4000),(27949057,282225,1000,0),(28213774,282233,500,0),(28265886,288143,1057000,0),(28265886,288163,197000,0),(28745352,285471,3895000,0),(29680791,282233,1000,0),(30353119,288141,414500,0),(30838180,288161,565000,2000),(31343445,288049,3343000,128000),(31489421,282289,50,0),(31489421,288115,4128500,0),(31770250,283935,1066000,0),(31770250,288077,815000,0),(31979237,286725,57000,0),(32764682,282229,970,10),(33004285,288175,284000,8000),(33233147,288115,782500,0),(33785940,288077,3002000,0),(34040630,288141,1617164,64000),(34439946,288173,243000,2000),(35076511,282223,1,0),(36701088,285471,1752000,0),(36797735,288163,271000,2000),(36994643,282227,815,5),(37149011,282245,48000,1000),(37985286,286721,830000,0),(38623487,282223,7933,10),(38750015,282273,3405,20),(39570216,288049,2704500,128000),(39767591,282239,24850,50),(39983520,285471,30000,0),(40421711,288165,197000,0),(40591466,288143,0,164500),(40689109,287805,1000,0),(40816146,282273,6030,10),(42090449,286725,60000,0),(42265344,286721,1936500,0),(42551351,282221,4540,5),(42744687,282225,970,0),(43407565,282227,480,20),(44097167,282239,45950,0),(44137405,282227,0,0),(44137405,282235,970,10),(44179539,282233,46,0),(45382627,283207,414000,0),(45623115,282241,0,1000),(45657531,282229,935,0),(45657531,282241,1357,0),(45701407,282273,480,20),(45741614,282221,3275,0),(45816656,286725,1757750,0),(45912430,285471,1670000,0),(45912430,288089,115000,0),(45912430,288141,115000,0),(46658760,285845,285000,0),(46710086,283203,19000,0),(46907003,282235,880,0),(47247878,285471,79500,0),(47769865,282223,490,10),(48131663,288161,195000,0),(48168009,283935,167000,0),(48427142,282223,7299,0),(48451621,282245,105000,0),(48544175,282233,2125,10),(48835177,282247,955,5),(49280041,282221,950,0),(49390740,282225,590,0),(49430288,283207,123000,0),(49913744,282235,990,10),(50351439,288143,8817336,0),(50371593,287811,1000,0),(50470929,286721,30000,0),(50470929,288161,550000,2000),(50692367,288169,194000,0),(51043018,282227,1923,10),(51046371,282223,905,10),(51214161,286721,45000,0),(51266031,288171,104000,8000),(51398390,282273,965,10),(51521727,288169,222000,4000),(51683694,288143,613500,256000),(51784024,283203,146000,0),(51878474,282241,7050,1000),(52123464,282235,990,0),(52123464,282245,3850,0),(52149614,282245,71175,21438),(52619230,288163,176500,0),(53351177,285845,188000,0),(53351177,288097,205000,128000),(53371964,285837,236000,0),(53371964,288089,557000,32000),(53379187,288097,155000,0),(53426163,282227,0,0),(53646371,288177,267500,1000),(53702790,288125,1740000,0),(54026246,282225,1470,10),(54072301,282247,985,15),(54087388,286721,2469000,0),(54445772,285471,1160000,0),(54445772,285845,660000,0),(54445772,288141,0,53000),(54703496,285845,426000,0),(54703496,286729,1284500,0),(54703496,288125,82500,0),(54703496,288143,20000,0),(54997057,286721,657000,0),(55115991,282227,2650,10),(55228368,288163,128000,0),(55368306,282229,990,20),(55618980,288077,744000,128000),(55654287,288089,447000,0),(55654287,288165,191000,2000),(55656569,288089,104000,16000),(55672549,288163,195000,0),(55725501,288169,193000,4000),(55809847,282231,1000,0),(55827351,288143,385000,0),(55833270,286721,1237500,0),(55936763,282223,1515,10),(55967630,282239,2950,100),(56258486,285837,139000,0),(56356220,282239,0,0),(56356220,286725,10000,0),(56541664,285837,148000,0),(56601146,282247,960,0),(56659062,285837,2038500,0),(56717196,283935,421000,0),(56717196,286729,779500,0),(56781893,285837,143000,0),(56781893,288161,497000,0),(56839909,283207,712000,0),(56839909,288125,120000,0),(56864104,288125,52500,0),(57083845,288115,2171000,0),(57083845,288141,74000,64000),(57210921,282239,3521,0),(57331035,282245,298562,21438),(57348476,288175,92000,16000),(57355007,282241,17700,100),(57390284,288169,196000,0),(57425594,288143,3606500,0),(57449412,283935,1954500,0),(57495678,282231,1840,0),(57539182,282273,1841,20),(57565146,285845,347000,0),(57611907,285845,554000,0),(57622344,288173,153000,2000),(57850393,283207,462500,0),(57850393,288163,323000,2000),(58041419,282225,1325,0),(58041419,282247,825,0),(58053301,283207,640500,0),(58086919,288169,197000,0),(58097726,282245,215062,14938),(58177733,283935,187000,0),(58177733,285845,404000,0),(58373211,283935,181000,0),(58387498,283935,171000,0),(58387498,286729,1557000,0),(58494507,285837,921000,0),(58525063,283207,155000,0),(58525063,286725,288500,0),(58525063,288049,2899500,0),(58536662,282237,41726,0),(58544362,282233,990,10),(58555774,282245,0,14938),(58724729,286725,50000,0),(58857563,286721,105000,0),(58924669,288169,201000,0),(59028814,286725,286500,0),(59038351,286729,1311750,0),(59056985,282227,2533,20),(59136096,288165,208000,0),(59142663,285471,952500,0),(59212293,282225,1750,0),(59242196,288089,81000,0),(59285139,286729,369000,0),(59386514,288165,12000,0),(59411169,288163,504500,1000),(59596529,288141,749500,64000),(59611482,282231,990,0),(59611482,288171,189000,2000),(59628840,283203,9000,0),(59628840,288141,131000,0),(59683714,288161,197000,0),(59690659,288169,420000,4000),(59771943,288165,194000,0),(59798616,282247,250,10),(59857196,288097,85000,0),(59937358,282245,49500,0),(59946135,288089,111000,32000),(59965000,288169,193000,4000),(60185307,282237,32000,0),(60185307,282245,100000,0),(60210827,286729,1195500,0),(60285907,282221,3315,0),(60411553,282229,5126,20),(60562122,283207,314000,0),(60588234,288141,59000,0),(60639771,288115,75000,0),(60669825,282247,990,10),(60711981,282231,4355,0),(60711981,282233,990,10),(60739254,282225,3045,0),(60739254,286725,1189500,0),(60804380,288115,461500,100000),(60826215,285471,294000,0),(60849456,286729,42500,0),(60870281,283935,177000,0),(60870281,288115,433500,200000),(60900661,288097,168000,0),(60930777,285837,693500,0),(60930777,288165,627000,4000),(60968398,288161,399000,0),(60975210,282227,0,0),(61032645,288115,1967500,0),(61043050,282235,927,5),(61122885,288177,129500,2000),(61131538,282229,1000,0),(61131538,282237,0,0),(61213044,282241,9158,1000),(61253953,283207,153000,0),(61267204,288077,2569000,256000),(61267204,288141,1197000,0),(61372052,288097,1075000,64000),(61376254,282233,0,0),(61452657,282233,3276,10),(61497454,287805,0,0),(61497454,287815,1000,0),(61520151,282245,50000,0),(61560675,282231,0,0),(61620823,282231,2365,0),(61662777,283935,1677500,0),(61672793,283203,1467500,0),(61677994,285471,56000,0),(61736214,288125,1043500,150000),(61796213,285471,111000,0),(61796213,288141,59000,0),(61931973,288125,2005000,0),(61948429,282221,985,15),(62060753,288125,742500,150000),(62060753,288165,193000,0),(62089120,283207,139000,0),(62089120,286725,40000,0),(62122075,288165,196000,0),(62130680,282273,975,0),(62206716,282229,1571,0),(62232549,282223,4090,10),(62276737,282225,8430,0),(62306088,288125,787500,0),(62325946,288097,4442500,128000),(62358072,282223,0,0),(62358072,282225,6685,5),(62411115,286721,602500,0),(62456331,285845,121000,0),(62476700,282235,990,10),(62520119,283203,632000,0),(62543034,288171,689000,8000),(62545175,282221,150,0),(62582162,286729,5000,0),(62590817,282229,170,0),(62606216,288077,2230000,256000),(62710752,288169,533000,0),(62718489,282233,985,5),(62769655,283203,2674000,0),(62805331,283203,870500,0),(62807316,288089,2022500,32000),(62931329,282225,700,0),(62938248,282237,2950,0),(62947419,286721,251500,0),(62960564,282237,2050,0),(63002210,282229,1000,0),(63008664,288143,71000,0),(63008664,288163,200000,0),(63024776,288143,348000,0),(63038042,282221,990,10);