from lxml import html

from StockStcn.base_stcn import STCN_Base
from StockStcn import stcn_utils as utils


class STCN_DaPan(STCN_Base):
    # 大盘
    def __init__(self):
        super(STCN_DaPan, self).__init__()
        self.format_url = "http://stock.stcn.com/dapan/{}.shtml"
        self.pages = True  # 是否需要翻页
        self.page_num = 21
        self.name = '大盘'

    def _parse_list_body(self, body):
        # print(body)
        doc = html.fromstring(body)
        items = utils.parse_list_items_3(doc)
        [self._add_article(item) for item in items]
        # print(len(items))
        return items


if __name__ == "__main__":
    dapan = STCN_DaPan()
    dapan._start()
