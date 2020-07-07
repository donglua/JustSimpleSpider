import time

import schedule

from JfInfo.jfinfo_main import JFSchedule
from Takungpao.takungpao_main import TakungpaoSchedule
from base import SpiderBase
from configs import LOCAL


class MainSwith(SpiderBase):
    def __init__(self):
        super(MainSwith, self).__init__()
        self.tables = list()

    def ding_crawl_information(self):
        self._spider_init()
        print(self.tables)
        msg = ''
        for table, dt_benchmark in self.tables:
            sql = '''SELECT count(id) as inc_count FROM {} WHERE {} > date_sub(CURDATE(), interval 1 day);'''.format(table, dt_benchmark)
            inc_count = self.spider_client.select_one(sql).get("inc_count")
            msg += f'{table} 今日新增 {inc_count}\n'

        if not LOCAL:
            self.ding(msg)
        else:
            print(msg)

    def start_task(self, cls, dt_str, at_once=1):
        def task():
            cls().start()

        self.tables.append((cls.table_name, cls.dt_benchmark))
        if at_once:    # 是否立即执行一遍
            task()
        schedule.every().day.at(dt_str).do(task)

    def run(self):
        self.start_task(TakungpaoSchedule, "00:00", 0)

        self.start_task(JFSchedule, '01:00', 0)

        self.ding_crawl_information()
        schedule.every().day.at("17:00").do(self.ding_crawl_information)

        while True:
            schedule.run_pending()
            time.sleep(10)


if __name__ == "__main__":
    ms = MainSwith()
    ms.run()