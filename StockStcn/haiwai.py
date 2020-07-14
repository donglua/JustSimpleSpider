# from lxml import html
#
# from StockStcn.base_stcn import STCN_Base
# from StockStcn import stcn_utils as utils
#
#
# class STCN_HaiWai(STCN_Base):
#     # 海外
#     def __init__(self):
#         super(STCN_HaiWai, self).__init__()
#         self.format_url = "http://news.stcn.com/xwhw/{}.shtml"
#         self.pages = True  # 是否需要翻页
#         self.page_num = 21
#         self.name = '海外'
#
#     def _parse_list_body(self, body):
#         # print(body)
#         # sys.exit(0)
#         doc = html.fromstring(body)
#         items = utils.parse_list_items_1(doc)
#         [self._add_article(item) for item in items]
#         # print(len(items))
#         return items
#
#
# if __name__ == "__main__":
#     haiwai = STCN_HaiWai()
#     haiwai._start()
