#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File    : pangu.py
@Time    : 2020/10/9 14:58
@Author  : zhouj
@Email   : zhoujin9611@163.com
@phone   : 13937158462
@Software: PyCharm
"""
import numpy as np
import pandas as pd
import AiPangu.tools as pg_tools
from AiPangu.check_params import *


def get_k_info(code: str = None, k_type: str = "gg", st_date: str = None, en_date: str = None, retry: int = 3, pause: float = 0.01) -> pd.DataFrame:
    """
    获取个股历史交易记录
    Parameters
    ------
        code:string 股票代码 e.g. 600848
        k_type:string 要获取个股k线还是指数k线，"gg" - 个股，"zs" - 指数
        st_date:string 开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
        en_date:string 结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
        retry : int, 默认 3 如遇网络等问题重复执行的次数
        pause : int, 默认 0.01 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          'date', 'open', 'high', 'close', 'low', 'volume'
           日期 ，  开盘价，  最高价，  收盘价，  最低价， 成交量
    """


def get_rank_list_chosen_stocks(number: str = '0001', st_idx: int = 1, en_idx: int = 30, retry: int = 3, pause: float = 0.01) -> list:
    """
    获取排行的选股，返回选好的股票
    :param number: 选股方式，暂时只支持 0001（综合选股）,0002（技术选股）,0003（热点选股）
    :param retry: int, 默认 3 如遇网络等问题重复执行的次数
    :param pause: int, 默认 0.01 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    :param st_idx: 开始的序号
    :param en_idx: 结束的序号
    :return: ["000001",...]
    """


def get_default_chosen_stocks(retry: int = 3, pause: float = 0.01) -> list:
    """
    获取默认的选股，供给回测使用
    目前选用300开头股票（创业板）和600开头股票（上证一部分）
    :return:股票列表
    """


def get_business_days(bourse: str = None, st_date: str = '2018-01-01', en_date: str = '2018-12-31', retry: int = 3, pause: float = 0.01) -> list:
    """
    获取交易日历
    :param bourse: 交易所 默认SSE 上交所,   SZSE 深交所,  CFFEX 中金所,
                         SHFE 上期所,  CZCE 郑商所,  DCE 大商所,
                         INE 上能源,   IB 银行间,    XHKG 港交所
    :param st_date: 开始日期
    :param en_date: 结束日期
    :param retry: int, 默认 3 如遇网络等问题重复执行的次数
    :param pause: int, 默认 0.01 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    :return:
    """


class BackTesting:
    """回测结果要有：累计收益，年化收益，交易胜率，最大回撤"""

    def __init__(self):
        """初始化数据"""
        self.dict_bs_info = {}
        self.business_dates_info = dict()
        self._initial_capital = 1000000.0  # 初始资金，考虑到可能会有贵州茅台，初始资金设置大些
        self.num_of_shares = 0  # 持股数
        self._balance = self._initial_capital  # 余额

    def init_params(self):
        """初始化数据"""

    def trading_rule(self, stock: str) -> dict:
        """
        交易规则，规则自定义，要求：输入股票代码，输出买卖点
        :param stock:股票代码
        :return:买卖点，格式：字典格式，"b" - 买，"s" - 卖
                    {
                        "date1": ["b", "close_price"],
                        "date2": ["s", "close_price"],
                        "date3": ["b", "close_price"],
                        "date4": ["s", "close_price"],
                        ...
                    }
        """
        # 获取k线信息

    def stock_chosen_rule(self) -> list:
        """
        选股规则，规则自定义
        :return:选股信息，格式：字典格式
                    {
                        "date1": ["stock1", "stock2", "stock3", ...],
                        "date2": ["stock1", "stock4", "stock7", ...],
                        "date3": ["stock2", "stock5", "stock8", ...],
                        ...
                    }
        """

    def calc_win_rate(self, bs_info: dict) -> float:
        """
        计算交易胜率
        :param bs_info:交易信息 - {
                                    "date1": ["b", "close_price"],
                                    "date2": ["s", "close_price"],
                                    "date3": ["b", "close_price"],
                                    "date4": ["s", "close_price"],
                                    ...
                                }
        :return:交易胜率，保留两位小数
        """

    def calc_indicators(self, stock: str, b_days_key: int, st_date: str, en_date: str, bs_info: dict) -> tuple:
        """
        计算回测报告的指标，累计收益，年化收益，交易胜率，最大回撤
        :param bs_info:{
                            "date1": ["b", "close_price"],
                            "date2": ["s", "close_price"],
                            "date3": ["b", "close_price"],
                            "date4": ["s", "close_price"],
                            ...
                        }
        :param stock: 股票代码
        :param b_days_key: 每个时间段的key 1,2,...
        :param st_date: 起始时间
        :param en_date: 结束时间
        :return: 交易胜率，总收益，年化收益，最大回撤，每日收益
        """

    def calc_max_drawdown(self, earning_list: list) -> float:
        """
        计算最大回撤率
        :param earning_list: 收益列表
        :return: 最大回撤
        """

    def get_k_basic_data(self, stock: str, st_date: str = None, en_date: str = None) -> tuple:
        """
        获取一直股票一段时间内的k线基础数据
        :param st_date:开始日期
        :param en_date:结束日期
        :param stock:股票代码
        :return: 'date', 'open', 'high', 'close', 'low', 'volume'
           (日期 ,开盘价,最高价,收盘价, 最低价,成交量)
        """

    def get_cut_bs_info(self, st_date: str, en_date: str, bs_info: dict) -> dict:
        """
        根据回测的时间段，截取对应时间段的买卖点
        :param st_date:开始日期
        :param en_date:结束日期
        :param bs_info:
        :return:{
                    "date1": ["b", "close_price"],
                    "date2": ["s", "close_price"],
                    "date3": ["b", "close_price"],
                    "date4": ["s", "close_price"],
                    ...
                }
        """

    def get_back_testing_result(self, chosen_stocks: list) -> dict:
        """
        获取回测结果，所有选股在6个时间段内的测试结果
        :param chosen_stocks:选股列表 [股票代码]
        :return: 回测的结果
        """

    def handle_result(self, dict_back_testing: dict) -> dict:
        """
        处理回测结果
        :param dict_back_testing: {"win_rate":[], "daily_earnings":[]}
        :return: 回测结果
        """

    def get_business_dates(self) -> None:
        """
        获取六个回测时间段的交易时间，存到字典里
        """

    def run(self) -> dict:
        """入口函数"""


if __name__ == '__main__':
    pass
