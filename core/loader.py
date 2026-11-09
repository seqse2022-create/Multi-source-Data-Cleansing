import pandas as pd
import os


def ad_path(re_path:str)->str:
    """将相对路径转为绝对路径"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fp = os.path.join(BASE_DIR, re_path)
    return fp


def read_df(fp,logger)->list[list]|None:
    """分开读取sheet,返回df列表"""
    try:
        sheets = pd.read_excel(fp, sheet_name=None).items()
    except FileNotFoundError as e:
        logger.critical(f"文件路径错误:{e}")
        return None
    sheets_list=[]
    for name,df in sheets:
        if name=='院校清单':
            df = pd.read_excel(fp, sheet_name="院校清单", header=2)
            sheets_list.append([name,df])
        else:
            sheets_list.append([name,df])
    return sheets_list
if __name__ =="__main__":
    fp=ad_path("data/raw/招生单位_脏数据.xlsx")
    n=1
    sheets_list=read_df(fp,n)
    print(sheets_list)