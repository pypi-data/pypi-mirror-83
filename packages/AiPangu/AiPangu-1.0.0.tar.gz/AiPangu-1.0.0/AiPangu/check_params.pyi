# -*- encoding: utf-8 -*-
"""
@File    : check_params.py
@Time    : 2020/10/16 9:55
@Author  : gongyunpeng
@Email   : gypgongyunpeng@163.com
@Phone   : 13898107653
@Software: PyCharm
"""


def check_code(code: str) -> None:
    """检查股票代码，过滤掉非6位数字的代码"""


def check_date(date: str) -> None:
    """检查时间格式，年月日为xxxx-xx-xx格式"""


def check_idx(index: int) -> None:
    """检查索引"""


def check_bs_info(bs_info: dict) -> dict:
    """
        检查买卖点是否正确，保证第一个是买，最后一个是卖，且买卖点交替并且总个数为偶数
    :param bs_info:生成的买卖点信息
    :return: 检查后的买卖点信息
    """


if __name__ == '__main__':
    dd = {
        "2020-01-03": ["b", 12.3],
        "2019-01-03": ["b", 12.4],
        "2019-01-08": ["b", 12.4],
        "2019-01-01": ["b", 12.4]
    }
    check_bs_info(dd)
