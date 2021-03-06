import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

current_path = os.path.dirname(__file__)
origin_data = current_path + "/data.csv"

dept_cols = "分組"
group_cols = "組別"
id_cols = "學號"

cls_cols = "班級"
grade_cols = "入學學年"
# output = 1 科
predict_cols = "技術專題(二)"
# input = 13 科
subject_cols = [
    "微積分(一)", "微積分(二)", "電路學(一)", "電路學(二)", "電子學(一)",
    "電機機械(一)", "電子學實習(一)", "計算機概論", "邏輯設計",
    "計算機程式設計", "資料結構", "電機機械實習"
]
# 每筆預測分別需要 平均值、標準差、電力組迴歸式、控制組迴歸式、資通組迴歸式
type_values = ['AVG', 'STDEV', 'LINEAR_A', 'LINEAR_B', 'LINEAR_C']


def data_preprocessing():
    # 讀取 csv 到資料表
    df = pd.read_csv(origin_data)
    # 篩選欄位 (分組、組別、學號、班級、入學學年、各科成績)
    df = df[[dept_cols, group_cols, id_cols, grade_cols, cls_cols] + subject_cols + [predict_cols]]

    # 取出入學學年的年份 ( 103, 104 ... )
    year_list = sorted(list(set(df[grade_cols])))
    # 分別取出每個入學學年的年份
    for year in year_list:
        # 取出該入學學年有的班級 ( 1, 2, 3 )
        cls_list = sorted(list(set(df[(df[grade_cols] == year)][cls_cols])))
        # 分別取出每個班級，並將原始分數計算成為標準分數
        for cls in cls_list:
            # 建立新資料表存放同班級學生
            target_df = df[(df[grade_cols] == year) & (df[cls_cols] == cls)].copy()
            # 計算各個科目的標準分數
            for sub in subject_cols:
                # 將標準分數直接覆蓋在原始分數上
                target_df.loc[:, sub] = calc_z_score(target_df[sub])
                # 將結果存回原本的資料表
                df[(df[grade_cols] == year) & (df[cls_cols] == cls)] = target_df

    # 取出分組的類別 ( A, B, C )
    dept_list = sorted(list(set(df[dept_cols])))
    # 分別取出每個分組，並將原始分數計算成為標準分數
    for dept in dept_list:
        # 建立新資料表存放同分組學生
        target_df = df[df[dept_cols] == dept].copy()
        # 將標準分數直接覆蓋在原始分數上
        target_df.loc[:, predict_cols] = calc_z_score(target_df[predict_cols])
        # 將結果存回原本的資料表
        df[df[dept_cols] == dept] = target_df

    return df


def calc_z_score(input_df):
    if np.std(input_df):
        return (input_df - np.mean(input_df)) / np.std(input_df)
    else:
        return 0.0


def linear_regression(input_data):
    coef = []
    # 取出分組的類別 ( A, B, C )
    team_list = sorted(list(set(input_data[dept_cols])))
    # 分別取出所有分組，訓練每個分組的線性迴歸
    for index, topic_team in enumerate(team_list):
        # 建立新的資料表存放同分組學生
        target_df = input_data[input_data[dept_cols] == topic_team].copy()
        # 取出 data 和 label 來訓練
        data = np.array(target_df[subject_cols])
        label = np.array(target_df[predict_cols])
        # 建立線性迴歸模型
        LR = LinearRegression()
        # 訓練模型
        LR.fit(data, label)

        # 取得線性迴歸係數與截距
        buffer = [type_values[2 + index]]
        for sub_coef in list(LR.coef_):
            buffer.append(round(sub_coef, 6))
        buffer.append(round(LR.intercept_, 6))
        coef.append(buffer)

    return coef


def get_mean_std():
    # 讀取 csv 到資料表
    df = pd.read_csv(origin_data)
    # 建立新串列，用來存放平均值與標準差
    avg_std = []
    row_counter = 0
    # 取出入學學年的年份 ( 103, 104 ... )
    year_list = list(dict.fromkeys(df[grade_cols]))
    # 分別取出每個班級，
    for year in year_list:
        # 取出該入學學年有的班級 ( 1, 2, 3 )
        cls_list = list(dict.fromkeys(df[(df[grade_cols] == year)][cls_cols]))
        # 分別取出每個班級
        for cls in cls_list:
            avg_list = []
            std_list = []
            # 建立新資料表存放同班級學生
            target_df = df[(df[grade_cols] == year) & (df[cls_cols] == cls)].copy()
            # 計算各個科目的平均值和標準差
            for sub in subject_cols:
                avg_list.append(round(np.mean(target_df[sub]), 4))
                std_list.append(round(np.std(target_df[sub]), 4))
            row_counter += 1
            avg_std.append([row_counter, year, cls, type_values[0]] + avg_list + [np.float64(0)])
            row_counter += 1
            avg_std.append([row_counter, year, cls, type_values[1]] + std_list + [np.float64(0)])
    return avg_std


if __name__ == "__main__":
    dataset = data_preprocessing()
    model = linear_regression(dataset)
    data_info = get_mean_std()

    result = []
    for i in range(0, len(data_info)):
        result.append(data_info[i])
    for i in range(0, len(model)):
        result.append([(len(data_info) + 1 + i), 0, 0] + model[i])

    print(result)
