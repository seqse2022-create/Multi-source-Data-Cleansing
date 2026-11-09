#因为运行代码脚本在bin所以bin为顶级包,只能绝对导入,可以用sys将项目文件导入环境,就可以用相对导入了
import os
import sys
import logging.config

BASE_DIR=os.path.dirname(os.path.dirname(__file__))#__file__获得文件绝对路径,os获取父级
sys.path.append(BASE_DIR)

from conf.settings import LOG_CONFIG,path_save,path_read,encoding,pat
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("logger_both")

from core.cleaner import cleaner
from core.loader import ad_path,read_df
from core.merger import merge_and_validate


def main():
    read_fp = ad_path(path_read)
    save_fp = ad_path(path_save)
    sheets_list = read_df(fp=read_fp,logger=logger)
    if sheets_list==None:
        return None
    df_list=[]
    
    for i in sheets_list:
        _,df=cleaner(df_list=i,logger=logger,pat=pat)
        df_list.append(df)
    
    df = merge_and_validate(*df_list, encoding=encoding, logger=logger, path_save=save_fp)
    print(f"完成：{len(df)} 行")
    print(df["203状态"].value_counts())
    print((df[df["省份"]=="广东"]))
if __name__ == "__main__":
    main()