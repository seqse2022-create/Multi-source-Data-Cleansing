import pandas as pd
import re
import logging.config
from core.cleaner import cleaner
from core.loader import ad_path
from conf.settings import LOG_CONFIG,path_save,path_read,encoding,pat
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("logger_both")



def test_清洗后行数是36(monkeypatch):
    df = pd.read_excel(ad_path(path_read), sheet_name="院校清单", header=2)
    name,df=cleaner(["院校清单",df],pat=pat,logger=logger)
    assert len(df)==36
    

def test_省份全部识别():
    df = pd.read_excel(ad_path(path_read), sheet_name="院校清单", header=2)
    name,df=cleaner(["院校清单",df],pat=pat,logger=logger)
    for idx, row in df[["所在地", "省份"]].iterrows():
        if not row["省份"]:
            continue
        assert re.fullmatch(pat, row["省份"])
        assert row["省份"] in row["所在地"]


