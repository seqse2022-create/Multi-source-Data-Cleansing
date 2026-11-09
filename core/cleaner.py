import pandas as pd

def cleaner(df_list:list,logger,pat:str)->list:
    """表格清洗"""
    name,df=df_list
    if name == "院校清单":
        logger.info(f"{name}第0步{df.shape[0]}")
        df = df.dropna(how="all")                                      # 删全空行
        logger.info(f"{name}第1步{df.shape[0]}")
        df = df[df["院校名称"].str.strip() != "合计"]                    # 删合计行
        logger.info(f"{name}第2步{df.shape[0]}")
        df["院校名称"] = df["院校名称"].str.replace("（北京）","",regex=False).str.strip()
        logger.info(f"{name}第3步{df.shape[0]}")
        s = df["所在地"]
        df["省份"] = s.str.extract(pat)
        logger.info(f"{name}第4步{df.shape[0]}")
        df["更新时间"] = df["更新时间"].str.replace("年", "-").str.replace("月", "-").str.replace("日", "")
        df["更新时间"]= pd.to_datetime(df["更新时间"], format="mixed", errors="coerce")
        logger.info(f"{name}第5步{df.shape[0]}")
        df=df.drop_duplicates(subset=["院校名称"],keep="first")
        logger.info(f"{name}第6步{df.shape[0]}")
        df=df.reset_index(drop=True)
        df["序号"] = range(1, len(df) + 1)
        logger.info(f"{name}第7步{df.shape[0]}")
    else:
        logger.info(f"{name}第0步{df.shape[0]}")
        df["院校名称"] = df["院校名称"].str.strip()
        logger.info(f"{name}第1步{df.shape[0]}")
        df=df.drop_duplicates(subset=["院校名称","专业代码"],keep="last")
        logger.info(f"{name}第2步{df.shape[0]}")
    return [name,df]