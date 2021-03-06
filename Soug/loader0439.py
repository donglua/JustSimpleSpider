import os
import pprint
import re
import sys
import traceback
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from lxml import html


from Soug.tools import startChinese, getChinese, byte2str, startPy, getPyTable

base_url = 'https://pinyin.sogou.com/dict/cate/index/{}'


def parse_pagenum(page):
    soup = BeautifulSoup(page, "html.parser")
    try:
        totalpagenum = soup.find(id='dict_page_list').find('ul').find_all('span')[-2].a.contents[0]
    except:
        totalpagenum = 1

    return totalpagenum


def parse_url_and_save(page, path):
    soup2 = BeautifulSoup(page, "html.parser")
    for kk in soup2.find_all('div', class_='dict_detail_block'):
        third_class = kk.find(class_='detail_title').find('a').contents[0]
        third_url = kk.find(class_='dict_dl_btn').a['href']
        print(third_class, third_url)
        file_path = os.path.join(path, "{}.scel".format(third_class))
        print(" " * 8 + "Level 3 :" + third_class + " " * 10 + "Downloading")
        try:
            urlretrieve(third_url, file_path, callbackfunc)
        except Exception:
            pass


def callbackfunc(blocknum, blocksize, totalsize):
    """
    回调函数
    :param blocknum: 已经下载的数据块
    :param blocksize:  数据块的大小
    :param totalsize: 远程文件的大小
    :return:
    """
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    sys.stdout.write("\r%6.2f%%" % percent)
    sys.stdout.flush()


needs = {
    # 城市信息
    180: '北京', 306: '上海', 324: '天津', 354: '重庆', 168: '安徽',
    174: '澳门', 186: '福建', 192: '甘肃', 198: '广东', 204: '广西',
    210: '贵州',  216: '海南',  222: '河北', 228: '河南',  234: '黑龙江',
    240: '湖北', 246: '湖南', 252: '吉林', 258: '江苏', 264: '江西',
    270: '辽宁',  276: '内蒙古', 554: '宁夏', 282: '青海',  288: '山东',
    294: '山西', 300: '陕西', 312: '四川', 318: '台湾', 330: '香港',
    336: '新疆', 555: '西藏',  342: '云南',  348: '浙江', 360: '全国',
    366: '国外地名',

    # 自然科学
    1: '自然科学',
        # 2: '数学',
        # 3: '物理',
        #     4: '电学', 5: '电磁学', 6: '光学', 7: '力学', 8: '声学',
        #     9: '热学', 10: '量子物理', 11: '生物物理', 12: '普通物理',
        #     552: '核物理',  630: '其他',
        #
        # 13: '化学',
        # 14: '生物',
        #     15: '动物', 16: '植物', 17: '微生物', 18: '分子生物学',
        #     19: '古生物学', 20: '昆虫学', 21: '生态学', 22: '生物化学',
        #     23: '生物信息学', 24: '普通生物学', 25: '细胞生物学',
        #
        # 26: '地理地质',
        # 27: '海洋学',
        # 28: '气象学',
        # 29: '天文学',
        # 30: '其它',

    # 社会科学
    76: '社会科学',
        # 77: '经济管理',
        #     78: '财务会计', 79: '管理科学与工程', 80: '金融保险', 81: '经济学',
        #     82: '人力资源与组织行为学',  83: '商务营销贸易',
        # 84: '公共管理',
        # 85: '法律',
        # 86: '广告传媒',
        # 87: '教育教学',
        # 88: '伦理学',
        # 89: '社会学',
        # 90: '心理学',
        # 91: '政治学',
        # 92: '档案学',
        # 93: '军事',
        # 94: '房地产',
        # 95: '其它',

    # 工程与应用科学
    96: '工程与应用科学',
        # 97: '计算机',
        #     98: '互联网', 99: '硬件', 100: '软件',
        #     101: '人工智能', 102: '计算机科技', 644: '其他',
        # 103: '电力电气',
        # 104: '电子工程',
        # 105: '船舶工程',
        # 106: '纺织服装',
        # 107: '钢铁冶金',
        # 108: '工业设计',
        # 109: '化工',
        # 110: '材料科学',
        # 111: '环境能源',
        # 112: '机械工程',
        # 113: '建筑',
        # 114: '交通运输物流',
        # 115: '矿业勘探',
        # 116: '汽车工程',
        # 117: '水利工程',
        # 118: '通信与无线电',
        # 119: '土木结构',
        # 120: '印刷印染',
        # 121: '造纸',
        # 122: '质量工程',
        # 123: '安全工程',
        # 124: '包装',
        # 125: '测绘工程与地图',
        # 126: '其它',

    # '农林渔畜'
    127: '农林渔畜',
        # 128: '林业',
        # 129: '农业',
        # 130: '畜牧业',
        # 131: '渔业',

    # 医学
    132: '医学',
        # 133: '基础医学',
        # 134: '西药学',
        # 135: '中医',
        # 136: '中药',
        # 137: '针灸',
        # 138: '疾病',
        # 139: '超声医学',
        # 140: '耳鼻喉科',
        # 141: '法医学',
        # 142: '护理学',
        # 143: '解剖学',
        # 144: '口腔医学',
        # 145: '美容外科',
        # 146: '皮肤科',
        # 147: '兽医',
        # 148: '医疗器械',
        # 149: '医学影像学',
        # 150: '肿瘤形态学',
        # 151: '医学检验',
        # 152: '医疗',
        # 550: '外科',
        # 153: '其它',

    # 电子游戏
    436: '电子游戏',
        # 437: '单机游戏',
        #     606: '角色扮演',
        #     607: '运动休闲',
        #     608: '射击游戏',
        #     609: '回合游戏',
        #     610: '策略经营',
        #     611: '其他',
        # 461: '网络游戏',
        #     612: '角色扮演',
        #     613: '运动休闲',
        #     614: '射击游戏',
        #     615: '回合游戏',
        #     616: '策略经营',
        #     617: '其他',
        #
        # 604: "网页游戏",
        #     618: '角色扮演',
        #     619: '运动休闲',
        #     620: '射击游戏',
        #     621: '回合游戏',
        #     622: '策略经营',
        #     623: '其他',
        #
        # 605: '手机游戏',
        #     624: '角色扮演',
        #     625: '运动休闲',
        #     626: '射击游戏',
        #     627: '回合游戏',
        #     628: '策略经营',
        #     629: '其他',

    # 艺术
    154: '艺术',
        # 155: '刺绣织染',
        # 156: '金属工艺',
        # 157: '书法篆刻',
        # 158: '雕塑',
        # 159: '绘画',
        # 160: '曲艺',
        # 161: '摄影',
        # 162: '陶瓷',
        # 163: '舞蹈',
        # 164: '音乐',
        #     165: '名家名作', 166: '音乐术语', 648: '其他',
        # 646: '其他',

    #  生活
    389: '生活',
        # 390: '理财',
        # 393: '家居装饰',
        # 394: '家用电器',
        # 395: '美容护肤',
        # 396: '习俗',
        # 397: '服饰',
        # 398: '礼品',
        # 399: '旅游',
        # 400: '日常',
        # 401: '办公文教',
        # 402: '饮食',
        # 551: '美发',
        # 650: '其他',

    # 运行休闲
    367: '运动休闲',
        # 368: '球类',
        #     369: '棒球', 370: '篮球', 371: '乒乓球',
        #     372: '足球', 652: '排球', 656: '其他',
        #
        # 373: '棋牌类',
        #     374: '麻将', 375: '围棋', 376: '象棋',
        #     377: '休闲牌类', 553: '桥牌',
        #
        # 378: 'F1赛车',
        # 379: '跆拳道',
        # 380: '太极拳',
        # 381: '气功',
        # 382: '武术',
        # 383: '奥运',
        # 384: '垂钓',
        # 385: '轮滑',
        # 386: '自行车',
        # 387: '杀人游戏',
        # 388: '其它',

    # 人文科学
    31: '人文科学',
        # 32: '历史',
        #     33: '历史地理', 34: '历史名人', 35: '世界历史',
        #     36: '中国古代史', 37: '中国近现代史', 634: '其他',
        #
        # 38: '文学',
        #     39: '红楼梦', 40: '经典名著', 41: '科幻', 42: '流行作品',
        #     43: '毛泽东诗词', 44: '民间文学', 45: '奇幻玄幻', 46: '三国演义',
        #     47: '诗词歌赋', 48: '实用写作', 49: '水浒传', 50: '武侠',
        #     51: '言情', 52: '其它',
        # 53: '语言',
        #     54: '成语', 55: '俗语', 56: '流行新词',
        #     57: '谜语', 58: '外语', 59: '网络流行用语',
        #     60: '语言学', 636: '其他',
        # 61: '哲学',
        #     62: '马克思主义哲学', 63: '西方哲学', 64: '中国哲学', 65: '哲学史', 638: '其他',
        #
        # 66: '宗教',
        #     67: '道教', 68: '佛教', 69: '基督教', 70: '伊斯兰教', 640: '其他',
        #
        # 71: '考古',
        # 72: '伦理学',
        # 73: '人类学',
        # 74: '神学',
        # 75: '其它',

    # 娱乐
    403: '娱乐',
        # 404: '动漫',
        #     405: '新番', 406: '网球王子', 407: '死神', 408: '守护甜心',
        #     409: '圣斗士', 410: '犬夜叉', 411: '叛逆的鲁鲁修', 412: '名侦探柯南',
        #     413: '乱马', 414: '家庭教师Reborn', 415: '机器猫', 416: '火影忍者',
        #     417: '海贼王', 418: '宠物小精灵', 666: '其他',
        # 420: '收藏',
        #     421: '古玩', 422: '邮票', 423: '字画', 424: '钱币', 425: '其它',
        # 426: '电影电视',
        # 427: '流行音乐',
        # 428: '时尚品牌',
        # 429: '明星',
        # 430: '模型',
        # 431: '魔术',
        # 432: '汽车',
        # 433: '烟草',
        # 434: '宠物',
        # 435: '其它'
}


def load():
    # _map = {}
    # 从 0 到  437
    # for cate in range(438):
    for cate in needs.keys():
        cate_url = base_url.format(cate)
        resp = requests.get(cate_url)
        if resp.status_code == 200:
            page = resp.text
            doc = html.fromstring(page)
            cate_info = doc.xpath("//div[@class='cate_title']")[0].text_content()
            cate_info = re.findall("“(.*)”分类下共有(.*)个词库", cate_info)[0]
            cate_name = cate_info[0]
            cate_total = int(cate_info[1])
            print("'{}': '{}', ".format(cate, cate_name))
            if needs[cate] != cate_name:
                print(">>>>>>>>>>>>>>>>>>>>>>>", cate)
            # _map[cate] = cate_name
            # path = os.path.join("./origin", cate_name)
            # os.makedirs(path, exist_ok=True)
            # page_num = int(parse_pagenum(page))
            # for page_num in range(1, page_num+1):
            #     print("page is {}".format(page_num))
            #     url = cate_url + "/default/{}".format(page_num)
            #     page = requests.get(url).text
            #     parse_url_and_save(page, path)
            #     print()
            #     print()


def mv_dirs():
    data_dir = '/Users/furuiyang/mydata/origin'
    for name in os.listdir(data_dir):
        if name in needs.values():
            command = 'mv /Users/furuiyang/mydata/origin/{}  /Users/furuiyang/gitzip/JustSimpleSpider/Soug/origin/'.format(name)
            print(command)
            try:
                os.system(command)
            except:
                traceback.print_exc()


def _check():
    data_dir = '/Soug/origin'
    for name in os.listdir(data_dir):
        if name not in list(needs.values()):
            print(name)
        else:
            print("ok")


def scel2txt(in_file, out_file):
    print('-' * 60)
    with open(in_file, 'rb') as f:
        data = f.read()
    print("词库名：", byte2str(data[0x130:0x338]))
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))
    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])

    words = getChinese(data[startChinese:])
    for word in words:
        with open(out_file, 'a+', encoding='utf-8') as file:
            file.write(word[2] + '\n')


def trans(source_dir, target_dir):

    def listfiles(ldir: str, r: bool = True):
        lst = []
        csv_dirs = os.listdir(ldir)
        for one in csv_dirs:
            one = os.path.join(ldir, one)
            if os.path.isdir(one):
                if r:
                    lst.extend(listfiles(one))
                else:
                    pass
            else:
                lst.append(one)
        return lst

    error_list = []
    lst = listfiles(source_dir)
    for file in lst:
        n_file = file.replace(source_dir, target_dir).replace(".scel", ".data_dir")
        n_file_dir = os.path.split(n_file)[0]
        os.makedirs(n_file_dir, exist_ok=True)
        print(file, ">>>>>>", n_file)
        try:
            scel2txt(file, n_file)
        except:
            error_list.append(file)
        print()

    print(error_list)


def main():
    origin = '/Users/furuiyang/mydata/needs'
    target = '/Users/furuiyang/mydata/final'
    trans(origin, target)


if __name__ == "__main__":
    main()