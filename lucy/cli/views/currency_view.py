from typing import List
from rich import print
# from rich import inspect
# from rich.panel import Panel
from rich.table import Table
from lucy.application.trading.flex import Currency

from .view import View

#TODO: Taka á mismunandi accounts, núna er þetta bara flex

class CurrencyView(View):
    def listi(self, currency: Currency, header: str=None) -> None:
        table = Table()
        if header:
            table.title = header

        cols = ["Type", "Balance Value", "Portfolio Value", "Collateral Value", "PnL", "Unrealized Funding", "Total Unrealized", "Available Margin"]
        for c in cols:
            table.add_column(f"[grey54]{c}")

        for c in currency:
            bVal = "{:>10}".format(f"{c.balanceValue:.2f}")
            pVal = "{:>10}".format(f"{c.portfolioValue:.2f}")
            cVal = "{:>10}".format(f"{c.collateralValue:.2f}")
            pnl = "{:>10}".format(f"{c.pnl:.2f}")
            uFunding = "{:>8}".format(f"{c.unrealizedFunding:.2f}")
            tUnrealized = "{:>8}".format(f"{c.totalUnrealized:.2f}")
            aMargin = "{:>8}".format(f"{c.availableMargin:.2f}")
            table.add_row(c.type, bVal, pVal, cVal, pnl, uFunding, tUnrealized, aMargin)
        print(table)


# USD
#    quantity: 100.28
#    value: 100.28
#    collateral: 100.28
#    available: 100.28
# BTC
#    quantity: 0.000754
#    value: 20.15
#    collateral: 19.55
#    available: 0.00
# initialMargin: 0
# balanceValue: 120.43
# initialMargin: 0
# initialMarginWithOrders: 0
# maintenanceMargin: 0
# balanceValue: 120.43
# portfolioValue: 120.43
# collateralValue: 119.83
# pnl: 0
# unrealizedFunding: 0
# totalUnrealized: 0
# totalUnrealizedAsMargin: 0
# availableMargin: 119.83
# marginEquity: 119.83
# type: multiCollateralMarginAccount