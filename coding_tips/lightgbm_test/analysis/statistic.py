from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LABEL_DICT = {"0":"负样本","1":"正样本"}

def calculate_label_statistic(df:pd.DataFrame,label_name:str):
    label = df[label_name]

    label_dict=  label.value_counts().to_dict()

    for k,v in label_dict.items():
        print(f"{LABEL_DICT[str(k)]}:{int(v)}")

    return label.value_counts().to_frame()

def general_sample_statistic(df:pd.DataFrame):

    return df.describe()


def calculate_null_statistic(df:pd.DataFrame):

    null_counts = df.isnull().sum()
    non_null_counts = df.notnull().sum()
    ratio = (non_null_counts/(non_null_counts+null_counts))*100

    concat = pd.concat([null_counts,non_null_counts,ratio],axis=1).reset_index()
    concat.rename(columns={"index":"字段",0:"空值数量",1:"非空数量",2:"饱和度"},inplace=True)

    print(concat)

    return concat



def heatmap(df:pd.DataFrame,label_name:str,save_name:Optional[str]=None):

    plt.figure(figsize=(18,14))
    x = df.drop(label_name,axis=1)
    sns.heatmap(round(x.corr(),2),cmap='Blues',annot=True)
    if save_name:
        save_dir = Path(__file__).absolute().parent.parent / f"assets/{save_name}.png"
        plt.savefig(save_dir)
    plt.show()


def swarmplot(df:pd.DataFrame,
              feature_list:List[str],
              label_name:str,
              sample_num:int=1000,
              save_name:Optional[str]=None):
    """
    散点图
    只适用于数值性特征和y值的关系比较
    可以看出数值的变化和y值有没有关系
    """
    df_sample = df.sample(sample_num)
    df.dropna(thresh=)
    feature = df_sample[feature_list]
    #进行标准化，标准化后的特征值均值为0，标准差为1，这样可以使得不同特征之间的数字范围相同
    feature_std = (feature-feature.mean()) / feature.std()
    label = df_sample[[label_name]]

    data=  pd.concat([label,feature_std],axis=1)

    data = pd.melt(data,id_vars=label_name,var_name="Features",value_name="Values")

    plt.figure(figsize=(10,6))

    sns.swarmplot(x='Features',y='Values',hue=label_name,data=data)

    plt.xticks(rotation=45)
    if save_name:
        save_dir = Path(__file__).absolute().parent.parent / f"assets/{save_name}.png"
        plt.savefig(save_dir)
    plt.show()

def filter_rows_min_nonull(df:pd.DataFrame,thresh:int=5):
    """移除所有列中少于阈值个非缺失值的行"""
    return df.dropna(thresh=thresh)
    
if __name__ == "__main__":
    data_path = 'data/high_diamond_ranked_10min.csv'
    df = pd.read_csv(data_path)
    calculate_label_statistic(df,label_name="blueWins")
    # heatmap(df,label_name='blueWins',save_name="heatmap")
    # swarmplot(df,feature_list=['blueWardsPlaced','blueWardsDestroyed'],label_name="blueWins")
    calculate_null_statistic(df)
