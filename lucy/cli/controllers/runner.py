import schedule
import time
from datetime import datetime

import lucy.application.events.bus as bus
from lucy.main_logger import MainLogger
from lucy.application.trading.exchange import Exchange
from lucy.model.interval import Intervals
from lucy.model.bot import DcaBot
from lucy.infrastructure.repos.bot_repository import BotRepository


class Runner(object):
    '''Starts Lucy, runs on a schedule, and executes the bots'''
    bots: list[DcaBot]

    def __init__(self):
        self.exchange = Exchange()
        self.bots = BotRepository().fetch_active_bots()
        # schedule.every().minute.at(":00").do(self.tick)
        schedule.every(10).seconds.do(self.tick)
        self.logger = MainLogger.get_logger(__name__)

        print(f"Runner initialized {len(self.bots)} bots")
        bots_names = [b.name for b in self.bots]
        bots_names = ", ".join(bots_names)
        self.logger.info(
            f"Runner initialized {len(self.bots)} bots: {bots_names}")

    def start(self):
        '''Start Lucy'''
        bots = [f"{b.name} {b.symbols} {b.interval}" for b in self.bots]
        mssg = "\n".join(bots)
        print(f"Starting Lucy. Listening for:\n{mssg}")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def tick(self):
        intervals = Intervals(datetime.now())
        for bot in self.bots:
            try:
                bot.tick(intervals, self.exchange)
                bus.publish(bot.events())
            except Exception as e:
                self.logger.error(
                    f"Tick: Error in bot {bot.name} {bot.interval}",
                    exc_info=True
                )
                self.logger.error(e)
