import pytest
import pandas as pd
import logging.config
from core.merger import merge_and_validate
from core.loader import read_df,ad_path
from core.cleaner import cleaner
from conf.settings import LOG_CONFIG,path_read,encoding,pat
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("logger_both")

@pytest.fixture
def 清洗结果(tmp_path):
    read_fp = ad_path(path_read)
    sheets_list = read_df(fp=read_fp, logger=logger)
    df_list = [cleaner(df_list=i, logger=logger, pat=pat)[1] for i in sheets_list]
    return merge_and_validate(*df_list, encoding=encoding,
                              logger=logger, path_save=tmp_path / "result.csv")
    
def test_三态分类正确(清洗结果):
    df = 清洗结果
    assert (df["203状态"]=="支持").sum() == 13
    assert (df["203状态"]=="不支持").sum() == 10
    assert (df["203状态"]=="无数据").sum() == 14
    

def test_总数守恒(清洗结果):
    df = 清洗结果
    assert (df["203状态"]=="支持").sum() +(df["203状态"]=="不支持").sum()+(df["203状态"]=="无数据").sum() == 37

def test_数据完整性只有一行缺失(清洗结果):
    """只有对外经济贸易大学缺院校信息；重复行保留错会导致缺失数变多"""
    df = 清洗结果
    assert (df["数据完整性"] == "缺院校信息").sum() == 1