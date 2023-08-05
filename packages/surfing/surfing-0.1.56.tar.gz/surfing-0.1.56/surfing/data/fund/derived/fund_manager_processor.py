
import pandas as pd
import numpy as np
import datetime
import traceback
import time
from typing import List, Dict, Optional
from functools import partial
from multiprocessing import Pool

from ....util.calculator import Calculator
from ...api.basic import BasicDataApi
from ...api.derived import DerivedDataApi
from ...wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector
from ...view.basic_models import FundNav, Fund_size_and_hold_rate, FundInfo
from ...view.derived_models import FundManagerInfo, FundManagerIndex, FundManagerScore
from .derived_data_helper import DerivedDataHelper, FUND_CLASSIFIER, normalize, score_rescale


class ManagerProcessor:

    INDEX_LIST = {'csi_boodfund': 'H11023.CSI', 'csi_f_hybrid': 'H11022.CSI', 'csi_f_qdii': 'H11026.CSI', 'csi_stockfund': 'H11021.CSI', 'mmf': 'H11025.CSI'}
    REPLACE_DICT = {'stock': 'H11021.CSI', 'bond': 'H11023.CSI', 'mmf': 'H11025.CSI', 'QDII': 'H11026.CSI', 'mix': 'H11022.CSI'}
    DATE_DICT = {'stock': '2007-01-01', 'bond': '2003-01-01', 'mmf': '2004-01-07', 'QDII': '2008-01-01', 'mix': '2007-01-01'}

    def __init__(self, data_helper: DerivedDataHelper):
        self._data_helper: DerivedDataHelper = data_helper
        self._basic_api = BasicDataApi()
        self._df_list: Dict[str, pd.DataFrame] = {}  # 基金经理指数
        self._rank_list: Dict[str, pd.DataFrame] = {}  # 基金经理评分

    def init(self, start_date=str, end_date=str):
        self._td: pd.DataFrame = self._basic_api.get_trading_day_list()
        self._td['datetime'] = self._td.datetime.map(str)
        self._td = self._td[(self._td.datetime >= start_date) & (self._td.datetime <= end_date)]
        print('load td done')

        with BasicDatabaseConnector().managed_session() as quant_session:
            fund_nav_query = quant_session.query(
                FundNav.fund_id,
                FundNav.adjusted_net_value,
                FundNav.datetime
            ).filter(
                FundNav.datetime >= start_date,
                FundNav.datetime <= end_date,
            )
            self._nav = pd.read_sql(fund_nav_query.statement, fund_nav_query.session.bind)
            self._nav = ManagerProcessor._clean_nav(self._nav, self._td)
            self._rate: pd.DataFrame = self._nav.pct_change(fill_method=None).loc[start_date:end_date]
            print('load nav done')

        with DerivedDatabaseConnector().managed_session() as quant_session:
            mng_query = quant_session.query(
                FundManagerInfo.mng_id,
                FundManagerInfo.start_date,
                FundManagerInfo.fund_id,
                FundManagerInfo.mng_name,
                FundManagerInfo.end_date)
            self._fm: pd.DataFrame = pd.read_sql(mng_query.statement, mng_query.session.bind)
            self._fm = ManagerProcessor._clean_fm(self._fm)
            print('load fm done')

        with BasicDatabaseConnector().managed_session() as quant_session:
            fund_size_query = quant_session.query(
                Fund_size_and_hold_rate.fund_id,
                Fund_size_and_hold_rate.datetime,
                Fund_size_and_hold_rate.size
            )
            self._scale: pd.DataFrame = pd.read_sql(fund_size_query.statement, fund_size_query.session.bind)
            self._scale = ManagerProcessor._clean_scale(self._scale, self._td).loc[start_date:end_date].bfill()
            print('load scale done')

        self._base_index: pd.DataFrame = self._basic_api.get_index_price(index_list=list(self.INDEX_LIST.keys()))
        self._base_index = self._clean_index(self._base_index, self._td).loc[start_date:end_date]
        print('load base index done')

        with BasicDatabaseConnector().managed_session() as quant_session:
            fund_info_query = quant_session.query(FundInfo)
        self._info: pd.DataFrame = pd.read_sql(fund_info_query.statement, fund_info_query.session.bind)
        print('load info done')

    @staticmethod
    def _gap_days(start: str, end: str) -> int:
        return (pd.to_datetime(end, infer_datetime_format=True) - pd.to_datetime(start, infer_datetime_format=True)).days

    @staticmethod
    def _rate_calc(x: pd.Series) -> pd.Series:
        return x.pct_change(fill_method=None)

    @staticmethod
    def _clean_nav(nav: pd.DataFrame, td: pd.DataFrame) -> pd.DataFrame:
        nav = nav.rename(columns={'adjusted_net_value': 'nav'})
        nav['datetime'] = nav.datetime.map(str)
        nav = nav.pivot(index='datetime', columns='fund_id', values='nav')
        nav = nav.reindex(nav.index.union(td.datetime.array))
        nav = nav.ffill() + nav.bfill() - nav.bfill()  # bfill之后为NaN的部分让ffill之后也变为NaN
        nav = nav.loc[nav.index.intersection(td.datetime.array), :]
        return nav.dropna(how='all').dropna(how='all', axis=1)

    @staticmethod
    def _clean_fm(fm: pd.DataFrame) -> pd.DataFrame:
        fm = fm.rename(columns={'mng_id': 'manager_id', 'mng_name': 'name', 'start_date': 'start', 'end_date': 'end'})
        fm['start'] = pd.to_datetime(fm.start).dt.strftime('%Y-%m-%d')
        fm['end'] = pd.to_datetime(fm.end).dt.strftime('%Y-%m-%d')
        fm = fm[fm.fund_id != 'not_exist'].copy()
        return fm

    @staticmethod
    def _clean_scale(scale: pd.DataFrame, td: pd.DataFrame) -> pd.DataFrame:
        scale = scale.rename(columns={'size': 'scale'})
        scale['datetime'] = scale.datetime.map(str)
        scale = scale.pivot(index='datetime', columns='fund_id', values='scale')
        scale = scale.reindex(scale.index.union(td.datetime.array)).ffill()
        scale = scale.loc[scale.index.intersection(td.datetime.array), :]
        return scale.dropna(how='all').dropna(how='all', axis=1)

    def _clean_index(self, index: pd.DataFrame, td: pd.DataFrame) -> pd.DataFrame:
        base_index = index.copy()
        base_index['index_id'] = base_index['index_id'].map(self.INDEX_LIST)
        base_index['datetime'] = base_index.datetime.map(str)
        base_index = base_index.pivot(index='datetime', columns='index_id', values='close')
        base_index = base_index.reindex(base_index.index.union(td.datetime.array))
        base_index = base_index.loc[base_index.index.intersection(td.datetime.array), :]
        return base_index.ffill().dropna(how='all').dropna(how='all', axis=1)

    @staticmethod
    def _lambda_func_1(single_fund_info: pd.DataFrame, x: pd.Series) -> pd.Series:
        result: List[pd.Series] = []
        for row in single_fund_info.itertuples(index=False):
            result.append(pd.Series((x.index >= row.start) & (x.index <= row.end), index=x.index))
        return pd.concat(result, axis=1).sum(axis=1) > 0

    def _index_calculation(self, manager: str, fund_kind: str, class_info: pd.DataFrame, rate_df: pd.DataFrame, index_rate: pd.DataFrame) -> Optional[pd.Series]:
        '''
        计算基金经理指数
        manager：基金经理的ID
        fund_kind：基金的分类（'stock', 'bond', 'money', 'mix', 'QDII'）
        replace_index：空窗期选择替代的指数的代码
        rate_df：基金日收益率的dataframe
        scale_df：基金规模的dataframe

        返回基金经理指数的Series，时间是从第一个产品的任职到最后一个产品的离职

        该指数由于bfill的原因不可回测
        replace_index为空时，空窗期按照_REPLACE_DICT中的指数来代替（如果没有指定基金的分类，按照沪深300的指数）
        基金规模按照上期季报的规模作为权重，如果没有之前的数据，则按照下期季报的规模作为权重
        如果该日基金净值缺失，则用之前的净值代替，如果历史上并没有该日的净值数据，那么在计算基金经理指数的过程中该基金产品不再拥有权重
        如果因该日基金净值缺失而导致该日基金经理没有基金产品可供计算指数，按照空窗期来处理
        '''
        m_info = class_info[class_info['manager_id'] == manager]
        if m_info.shape[0] == 0:
            # raise Exception('该经理没有相关基金产品')
            return
        m_start: str = m_info['start'].min()
        m_end: str = m_info['end'].max()
        unique_fund_ids = m_info['fund_id'].unique()
        rate: pd.DataFrame = rate_df.loc[m_start:m_end, unique_fund_ids]
        # 此指数不可回测
        scale: pd.DataFrame = self._scale.loc[m_start:m_end, unique_fund_ids]
        for fund_id in unique_fund_ids:
            single_fund_info: pd.DataFrame = m_info[m_info.fund_id == fund_id]
            rate.loc[:, fund_id] = rate[fund_id].where(partial(ManagerProcessor._lambda_func_1, single_fund_info), 0)
            scale.loc[:, fund_id] = scale[fund_id].where(partial(ManagerProcessor._lambda_func_1, single_fund_info), 0)
        scale = scale + rate - rate  # rate为NaN的地方也让scale变为NaN
        scale = scale.fillna(0)  # 这里在将NaN全变为0
        ratio = (rate * scale).sum(axis=1) / scale.sum(axis=1).replace(0, 1)
        if ratio.shape[0] == 0:
            return
        ratio = pd.Series(np.where(ratio, ratio, index_rate.loc[ratio.index[0]:ratio.index[-1]]), index=ratio.index).fillna(0)
        return np.exp(np.log(1 + ratio).cumsum())

    def _calc_part3(self, m_dict, class_fund, eval_date_dt):
        eval_date = eval_date_dt.isoformat()
        eval_start_date = (eval_date_dt - datetime.timedelta(days=365)).isoformat()
        self._do_calc_part3(eval_start_date, eval_date, m_dict, class_fund)

    def _do_calc_part3(self, eval_start_date: str, eval_date: str, m_dict, class_fund):
        _rank_list = {}
        _tm_part3_start = time.time()
        for class_name, index_id in self.REPLACE_DICT.items():
            the_eval_start_date = max(eval_start_date, self.DATE_DICT[class_name])
            class_df = self._df_list[class_name]
            bm = self._base_index[index_id]
            try:
                cols = class_df.loc[eval_date].dropna().index
            except KeyError:
                continue
            benchmark_stat_result = []
            for i in cols:
                df = class_df[i].loc[the_eval_start_date:].dropna()
                if df.shape[0] < 5:
                    continue
                dic = Calculator.get_manager_stat_result(df.index.array, df.array, bm.loc[df.index].array)
                dic['name'] = m_dict[i]
                dic['index'] = i
                benchmark_stat_result.append(dic)
            stats: pd.DataFrame = pd.DataFrame(benchmark_stat_result).set_index('index')
            fund_ids = self._fm['fund_id'].isin(class_fund[class_name])
            for row in stats.itertuples():
                stats.loc[row.Index, 'start_date'] = min(self._fm[self._fm['manager_id'].isin([row.Index]) & fund_ids]['start'])
                stats.loc[row.Index, 'trade_year'] = ManagerProcessor._gap_days(start=stats.loc[row.Index, 'start_date'], end=stats.loc[row.Index, 'end_date']) / 365
            rf = 1.025 ** (1 / 365) - 1
            cl_result = []
            for i in stats.index:
                df = class_df[i].loc[the_eval_start_date:].dropna()
                total = pd.concat([ManagerProcessor._rate_calc(bm.loc[df.index]) - rf, ManagerProcessor._rate_calc(df)], axis=1)
                total = total[total.notna().all(axis=1)]
                res = DerivedDataHelper._lambda_cl(total.to_numpy())
                cl_result.append(res)
            temp = pd.DataFrame(cl_result)
            stats = stats.assign(model_alpha=temp['alpha'].array, model_beta=temp['beta'].array)
            # 存进去原始数据而不是rank
            _rank_list[class_name] = stats
        _tm_part3_end = time.time()
        print(f' part3 cost time {_tm_part3_end - _tm_part3_start}')

        _tm_part4_start = time.time()
        for class_name in self.REPLACE_DICT.keys():
            try:
                stats = _rank_list[class_name].drop(columns=['name', 'start_date', 'end_date'])
                if class_name != 'money':
                    stats['score'] = score_rescale(normalize(stats['trade_year']) + normalize(stats['annualized_ret']) + normalize(stats['sharpe']) + normalize(-stats['mdd']) + normalize(stats['model_alpha']) + normalize(stats['model_beta']))
                else:
                    stats['score'] = score_rescale(normalize(stats['trade_year']) + normalize(stats['annualized_ret']) + normalize(-stats['annualized_vol']))
                stats = stats[stats.notna().any(axis=1)]
                stats = stats.rename_axis(index='manager_id').reset_index()
                stats['fund_type'] = class_name
                stats['datetime'] = eval_date
                self._data_helper._upload_derived(stats, FundManagerScore.__table__.name)
            except KeyError:
                pass
        _tm_part4_end = time.time()
        print(f' part4 cost time {_tm_part4_end - _tm_part4_start}')
        print(f'{eval_date} done, cost {_tm_part4_end - _tm_part3_start}')

    def calc(self):
        _tm_part1_start = time.time()
        class_fund = {}
        class_index: Dict[str, pd.DataFrame] = {}
        class_info: Dict[str, pd.DataFrame] = {}
        m_dict = dict(zip(self._fm['manager_id'].tolist(), self._fm['name'].tolist()))
        # 在每个资产类别下用收益率的index定义一个空的df
        for class_name, index_id in self.REPLACE_DICT.items():
            self._df_list[class_name] = pd.DataFrame(index=self._rate.index)
            fund = self._info[self._info['wind_class_2'].isin(FUND_CLASSIFIER[class_name])].fund_id
            info = self._fm.loc[self._fm['fund_id'].isin(fund), :]
            info = info[info['fund_id'].isin(self._rate.columns.intersection(self._scale.columns))]
            class_info[class_name] = info
            class_index[class_name] = self._base_index[index_id].pct_change(fill_method=None)
            class_fund[class_name] = fund
        _tm_part1_end = time.time()
        print(f' part1 cost time {_tm_part1_end - _tm_part1_start}')

        # 遍历每个基金经理
        _tm_part2_start = time.time()
        for m_id in m_dict.keys():
            # 遍历每个资产类别
            for class_name in self.REPLACE_DICT.keys():
                idx = self._index_calculation(m_id, class_name, class_info[class_name], self._rate, class_index[class_name])
                if idx is not None:
                    # 该资产类别下记录计算结果
                    self._df_list[class_name].loc[:, m_id] = idx
        for class_name in self.REPLACE_DICT.keys():
            self._df_list[class_name] = self._df_list[class_name].replace(0, np.nan).dropna(how='all')
        _tm_part2_end = time.time()
        print(f' part2 cost time {_tm_part2_end - _tm_part2_start}')

    def _preprocess_manager_index_df(self, x):
        df = x.drop(columns='fund_type').pivot(index='datetime', columns='manager_id', values='manager_index')
        self._df_list[x.fund_type.array[0]] = df.set_axis(df.index.astype(str))

    def do_score_history(self, start_date: str, end_date: str):
        self._td: pd.DataFrame = self._basic_api.get_trading_day_list()
        self._td['datetime'] = self._td.datetime.map(str)
        self._td = self._td[(self._td.datetime >= start_date) & (self._td.datetime <= end_date)]
        print('load td done')

        with DerivedDatabaseConnector().managed_session() as quant_session:
            mng_query = quant_session.query(
                FundManagerInfo.mng_id,
                FundManagerInfo.start_date,
                FundManagerInfo.fund_id,
                FundManagerInfo.mng_name,
                FundManagerInfo.end_date)
            self._fm: pd.DataFrame = pd.read_sql(mng_query.statement, mng_query.session.bind)
            self._fm = ManagerProcessor._clean_fm(self._fm)
            print('load fm done')

        self._base_index: pd.DataFrame = self._basic_api.get_index_price(index_list=list(self.INDEX_LIST.keys()))
        self._base_index = self._clean_index(self._base_index, self._td).loc[start_date:end_date]
        print('load base index done')

        with BasicDatabaseConnector().managed_session() as quant_session:
            fund_info_query = quant_session.query(FundInfo)
        self._info: pd.DataFrame = pd.read_sql(fund_info_query.statement, fund_info_query.session.bind)
        print('load info done')

        fund_manager_index: pd.DataFrame = DerivedDataApi().get_fund_manager_index().drop(columns='_update_time')
        print('load fund manager index done')
        fund_manager_index.groupby(by='fund_type', sort=False).apply(self._preprocess_manager_index_df)
        print('process fund manager index done')

        m_dict = dict(zip(self._fm['manager_id'].tolist(), self._fm['name'].tolist()))
        class_fund = {}
        for class_name, index_id in self.REPLACE_DICT.items():
            class_fund[class_name] = self._info[self._info['wind_class_2'].isin(FUND_CLASSIFIER[class_name])].fund_id
        print('all data done, to calc fund manager score day by day')

        eval_date_dt_list: List[datetime.date] = []
        min_date = fund_manager_index.datetime.min()
        for eval_date in self._td.datetime.sort_values(ascending=False).array:
            eval_date_dt = pd.to_datetime(eval_date, infer_datetime_format=True).date()
            if eval_date_dt < min_date:
                continue

            eval_date_dt_list.append(eval_date_dt)
            # eval_start_date_dt = eval_date_dt - datetime.timedelta(days=365)
            # self._calc_part3(eval_start_date_dt.isoformat(), eval_date_dt.isoformat(), m_dict, class_fund)
            # print(f'{eval_date_dt} done')

        p = Pool()
        for i in p.imap_unordered(partial(self._calc_part3, m_dict, class_fund), eval_date_dt_list, 16):
            pass
        print('all done, to close and join')
        p.close()
        p.join()

    def do_score_update(self, eval_date_dt: datetime.date):
        m_dict = dict(zip(self._fm['manager_id'].tolist(), self._fm['name'].tolist()))
        class_fund = {}
        for class_name, index_id in self.REPLACE_DICT.items():
            class_fund[class_name] = self._info[self._info['wind_class_2'].isin(FUND_CLASSIFIER[class_name])].fund_id
        self._calc_part3(m_dict, class_fund, eval_date_dt)

    def do_index_history(self, start_date: str, end_date: str, history: bool = False) -> List[str]:
        self.init(start_date, end_date)
        print('init done, to calc manager index')
        self.calc()
        for class_type, df in self._df_list.items():
            index_to_inserted = df.rename_axis(index='datetime', columns='manager_id').stack().rename('manager_index').reset_index()
            if not history:
                index_to_inserted = index_to_inserted[index_to_inserted.datetime == end_date]
            index_to_inserted['fund_type'] = class_type
            self._data_helper._upload_derived(index_to_inserted, FundManagerIndex.__table__.name)

    def process(self, end_date: str):
        failed_tasks = []
        try:
            end_date_dt: datetime.date = pd.to_datetime(end_date, infer_datetime_format=True).date()
            self.do_index_history('2005-01-01', end_date_dt.isoformat())
            self.do_score_update(end_date_dt)
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('fund_manager_processor')
        return failed_tasks


if __name__ == '__main__':
    fmis = ManagerProcessor(DerivedDataHelper())
    # fmis.process('2020-09-10')
    # fmis.do_index_history(start_date='2005-01-01', end_date='2020-09-07', eval_date='2020-09-07', eval_start_date='2005-01-01')
    # fmis.do_score_history(start_date='2005-01-01', end_date='2020-09-07')
