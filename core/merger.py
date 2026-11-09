

def merge_and_validate(df_left,df_right,logger,path_save,encoding):
    """合并两表,并且进行203判断,以及保存"""
    df = df_left.merge(df_right,on="院校名称",how="outer")#保留全部数据
    df["序号"] = df["序号"].astype("Int64")
    df = df.sort_values("序号", na_position="last").reset_index(drop=True)
    logger.info(df.shape[0])
    df["203状态"] = df["外语科目"].str.contains("203").map({True: "支持", False: "不支持"})
    df.loc[df["外语科目"].isna(), "203状态"] = "无数据"
    df["专业代码"] = df["专业代码"].astype("Int64").astype(str).str.zfill(6)
    df["数据完整性"] = df[["省份", "序号", "院校网站"]].isna().any(axis=1).map({True: "缺院校信息", False: "完整"})
    df.to_csv(path_save,encoding=encoding,index=False)
    return df
