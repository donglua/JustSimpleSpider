# -*- coding: utf-8 -*-
import time

import pymysql
import requests
# from configs import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, LOCAL_MYSQL_HOST, \
#     LOCAL_MYSQL_PORT, LOCAL_MYSQL_USER, LOCAL_MYSQL_PASSWORD, LOCAL_MYSQL_DB

from PublicOpinion.configs import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, LOCAL_MYSQL_HOST, \
    LOCAL_MYSQL_PORT, LOCAL_MYSQL_USER, LOCAL_MYSQL_PASSWORD, LOCAL_MYSQL_DB


try:
    # conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    conn = pymysql.connect(host=LOCAL_MYSQL_HOST, port=LOCAL_MYSQL_PORT, user=LOCAL_MYSQL_USER, passwd=LOCAL_MYSQL_PASSWORD, db=LOCAL_MYSQL_DB)

except Exception as e:
    raise

cur = conn.cursor()
cur.execute("""select id, link  from  eastmoney_carticle where article is  NULL;""")
delete_info = {r[0]: r[1] for r in cur.fetchall()}
cur.close()
conn.close()


# {1717: 'http://caifuhao.eastmoney.com/news/20200203193311525228570',
# 1719: 'http://caifuhao.eastmoney.com/news/20200203190002919615800',
delete_ids = []
for id, url in delete_info.items():
    status_code = requests.get(url).status_code
    print(status_code)
    if status_code == 200:
        pass
    elif status_code == 404:
        delete_ids.append(id)
    time.sleep(3)


print(delete_ids)

'''
[181537, 181537, 193119, 197631, 199413, 203923, 205995, 207145, 207369, 207645, 209049, 231203, 236515, 243769, 245495, 259007, 259249, 263111, 278419, 280111, 282559, 305655, 307495, 308589, 311695, 330625, 334519, 334611, 341679, 353841, 375963, 376571, 377405, 377735, 377883, 388533, 397269, 397999, 398235, 401649, 401749, 421047, 421055, 421611, 426401, 430057, 436599, 446015, 446683, 453715, 459025, 462105, 464797, 469595, 472693, 483051, 500725, 507065, 507147, 507183, 507195, 510961, 517819, 520035, 520111, 520175, 520177, 527819, 539555, 539559, 541573, 541591, 541665, 544381, 548873, 550751, 565313, 565317, 568067, 571855, 581423, 581429, 584319, 595825, 599943, 602557, 604069, 611223, 615549, 630941, 634625, 638291, 643287, 643363, 643369, 643375, 643385, 643411, 643413, 658151, 658977, 667009, 672443, 681007, 681009, 681011, 681013, 688121, 688287, 691571, 697323, 710847, 712479, 713141, 718479, 727431, 727897, 740763, 741469, 742059, 749079, 750745, 755459, 756955, 757699, 758097, 758665, 759991, 760935, 772225, 773779, 774661, 781169, 784111, 788921, 788925, 789033, 790601, 794145, 802621, 831113, 835221, 835371, 842367, 849063, 849347, 849573, 855085, 856181, 858135, 859781, 859795, 861285, 865881, 878835, 879637, 880319, 880321, 882795, 887145, 892393, 900595, 902575, 902765, 906819, 907191, 915671, 919143, 920307, 923741, 929765, 935359, 937241, 937903, 938999, 944263, 955671, 971609, 972659, 975483, 990565, 990971, 996901, 1007051, 1011717, 1012737, 1018593, 1019223, 1020151, 1028139, 1028151, 1028153, 1028157, 1031683, 1048473, 1055283, 1057629, 1067899, 1071939, 1082395, 1084515, 1085467, 1095415, 1095419, 1095421, 1095423, 1096003, 1104199, 1105453, 1105681, 1110251, 1122173, 1122451, 1127071, 1127125, 1127395, 1131691, 1136735, 1136841, 1141355, 1148395, 1148893, 1150049, 1150207, 1150393, 1157507, 1157829, 1162177, 1177329, 1185639, 1187675, 1190055, 1197929, 1197965, 1197971, 1207791, 1224921, 1230437, 1230649, 1253265, 1253461, 1254993, 1257765, 1264909, 1269131, 1275511, 1279375, 1279405, 1279415, 1279419, 1279421, 1287635, 1288573, 1288819, 1298825, 1300021, 1300565, 1302101, 1305385, 1314577, 1318327, 1322203, 1325575, 1332799, 1336791, 1338735, 1350459, 1360115, 1360819, 1365305, 1365399, 1369723, 1370065, 1382683, 1385829, 1390583, 1402891, 1402901, 1402931, 1402933, 1411537, 1416115, 1427057, 1429371, 1430921, 1432277, 1436089, 1438983, 1444799, 1447841, 1450271, 1450693, 1453559, 1454811, 1454821, 1466929, 1469117, 1469179, 1471439, 1471523, 1472959, 1475083, 1484215, 1484221, 1484235, 1495049, 1495417, 1498083, 1498085, 1498087, 1499159, 1499295, 1508293, 1508455, 1511385, 1515213, 1517885, 1520577, 1521941, 1523955, 1523957, 1523967, 1523981, 1531395, 1537289, 1537911, 1541657, 1541659, 1541663, 1541665, 1542035, 1544891, 1545053, 1548011, 1550281, 1556107, 1558289, 1558445, 1564825, 1573915, 1580837, 1581947, 1584113, 1591461, 1608301, 1618773, 1619097, 1622675, 1626467, 1626469, 1626479, 1626485, 1628823, 1628961, 1631837, 1631847, 1635843, 1640055, 1641351, 1641687, 1641699, 1644947, 1644971, 1647671, 1649065, 1650129, 1654445, 1655113, 1655135, 1655571, 1664053, 1665387, 1666391, 1672921, 1673685, 1674807, 1678395, 1681749, 1686065, 1694521, 1699057, 1699501, 1700427, 1707165, 1707181, 1708037, 1719273, 1721517, 1721727, 1724817, 1737069, 1746307, 1761843, 1765891, 1767849, 1767953, 1770305, 1774065, 1776143, 1780449, 1780455, 1782593, 1784337, 1793921, 1797235, 1801947, 1801949, 1802489, 1809669, 1820509, 1820519, 1820529, 1823245, 1823655, 1823661, 1833897, 1834425, 1837971, 1838111, 1846119, 1848457, 1854563, 1871533, 1876893, 1878585, 1887771, 1890701, 1898533, 1901229, 1903637, 1905755]
'''