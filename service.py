import sqlite3
import os
import train

MODEL = [[1, 103, 1, 'AVG', 64.0851, 58.0213, 68.0638, 64.9787, 62.6383, 75.4468, 77.5532, 79.0638, 64.4681, 71.1489, 69.4255, 70.5319, 83.4681, 0.0], [2, 103, 1, 'STDEV', 11.2719, 13.874, 9.8443, 10.3769, 8.8352, 9.7015, 10.097, 6.9325, 10.9444, 7.6991, 8.9341, 7.1425, 2.7121, 0.0], [3, 103, 2, 'AVG', 62.94, 59.1, 71.96, 63.26, 69.4, 59.8, 68.06, 84.44, 70.68, 66.68, 63.58, 68.46, 84.38, 0.0], [4, 103, 2, 'STDEV', 14.4242, 22.1181, 9.239, 16.1565, 10.3885, 20.1623, 13.8122, 4.1287, 8.3077, 7.8318, 14.5273, 12.8284, 2.7921, 0.0], [5, 103, 3, 'AVG', 62.898, 58.2857, 74.102, 70.7143, 62.2041, 66.1429, 70.0204, 82.8367, 67.7551, 67.2449, 52.8776, 85.0408, 78.8163, 0.0], [6, 103, 3, 'STDEV', 13.1293, 19.7804, 15.3825, 17.5987, 11.425, 12.289, 16.7643, 5.0116, 9.144, 9.488, 13.7924, 8.7481, 6.7783, 0.0], [7, 104, 1, 'AVG', 60.902, 57.3529, 58.1961, 72.1373, 60.3333, 72.098, 80.3922, 83.7647, 64.7059, 68.451, 65.451, 63.3333, 84.2549, 0.0], [8, 104, 1, 'STDEV', 14.4076, 20.7088, 17.5756, 14.6529, 19.2361, 11.3677, 11.1409, 5.5008, 11.354, 13.8384, 8.8767, 10.1666, 3.086, 0.0], [9, 104, 2, 'AVG', 63.3778, 57.8222, 67.1111, 63.2, 61.7333, 74.1778, 75.4889, 81.6667, 64.8889, 68.2222, 65.6444, 64.4, 80.7333, 0.0], [10, 104, 2, 'STDEV', 10.8552, 17.048, 13.2484, 16.3239, 15.9491, 13.3538, 12.5408, 7.4147, 14.8836, 11.3644, 14.4224, 15.0619, 5.7403, 0.0], [11, 104, 3, 'AVG', 63.3617, 62.0213, 70.2128, 68.5106, 72.2128, 70.3617, 65.4681, 84.9787, 70.1915, 65.2553, 43.5319, 82.8298, 70.7021, 0.0], [12, 104, 3, 'STDEV', 19.7456, 23.2035, 21.7852, 21.1679, 13.9527, 12.0043, 17.8192, 6.8401, 10.6264, 17.6255, 26.4783, 14.9001, 10.2395, 0.0], [13, 0, 0, 'LINEAR_A', -0.133128, 0.194707, 0.208779, -0.144442, -0.227288, 0.201349, 0.065525, 0.152054, 0.041561, -0.128268, 0.015236, 0.15357, 0.261066, -0.149233], [14, 0, 0, 'LINEAR_B', -0.004823, 0.024641, 0.049376, 0.085107, 0.051409, -0.038676, 0.265413, 0.034369, 0.098137, -0.146747, 0.136827, 0.139616, -0.096655, 0.05393], [15, 0, 0, 'LINEAR_C', 0.268187, -0.395828, 0.127944, 0.150973, -0.064408, -0.14738, 0.150051, 0.0497, -0.177976, 0.156445, 0.176922, 0.243911, -0.024533, 0.023599]]

current_path = os.path.dirname(__file__)
database = current_path + "/database.sqlite"

id_cols = "ID"
type_cols = "類型"

cls_cols = train.cls_cols
grade_cols = train.grade_cols
# output = 1 科
predict_cols = train.predict_cols
# input = 13 科
subject_cols = train.subject_cols
# 每筆預測分別需要 平均值、標準差、電力組迴歸式、控制組迴歸式、資通組迴歸式
type_values = train.type_values

def init():
    # 建立資料庫連線
    conn = sqlite3.connect(database)
    # 刪除舊資料表，先以字串方式表示
    delete_table = f"drop table if exists score"
    # 執行刪除
    conn.execute(delete_table)
    # 建立新資料表，先以字串連接方式表示，設定資料表所需欄位與屬性
    create_table = f"create table if not exists score (" \
                   f"'{id_cols}' int not null, '{grade_cols}' int default null, " \
                   f"'{cls_cols}' int default null, '{type_cols}' varchar default null, "
    # 將科目欄位與屬性以遞迴的方式添加
    for sub in subject_cols:
        create_table += f"'{sub}' float default null, "
    # 添加最後技術專題欄位與屬性
    create_table += f"'{predict_cols}' float default null)"
    # 執行建立
    conn.execute(create_table)
    # 插入資料，先以字串連接方式表示
    for model_col in MODEL:
        # 設定索引順序，資料表將會依照指定順序添加
        insert_data = f"insert into score ('{id_cols}', '{grade_cols}', '{cls_cols}', '{type_cols}', "
        # 將科目以遞迴方式添加到索引中
        for sub in subject_cols:
            insert_data += f"'{sub}', "
        # 將技術專題天加到索引中的最後
        insert_data += f"'{predict_cols}') values ("
        # 開始添加模型參數，以遞迴方式添加
        for index, models in enumerate(model_col):
            # 如果是類型，則設為字串
            if index == 3:
                insert_data += f", '{models}'"
            # 如果 >0 則在前面加逗號
            elif index:
                insert_data += f", {models}"
            # 如果 =0 則不加逗號
            else:
                insert_data += f"{models}"
        # 最後加括號收尾
        insert_data += f")"
        # 執行插入
        conn.execute(insert_data)
    # 提交資料庫
    conn.commit()
    # 關閉資料庫連線
    conn.close()


def predict(data):
    # 取得指定【入學年】和【班級】的每科分數【平均值與標準差】，還有線性迴歸模型的方程式
    avg, std, linear_a, linear_b, linear_c = get_model(data)
    # 初始化方程式結果
    sum_a, sum_b, sum_c = 0, 0, 0
    # 初始化學生每科的標準分數
    person_grade = []
    # 遞迴計算學生的每科標準分數，並且計算線性迴歸模型方程式 (y=ax+b)
    for sub_index, sub in enumerate(subject_cols):
        # 計算標準分數，(原始分數 - 平均值) / 標準差 = 標準分數 (Z-Score)
        z_score = (float(data[sub]) - float(avg[sub])) / float(std[sub])
        # 儲存每科的科目名稱、原始分數、班級平均值、班級標準差、標準分數
        person_grade.append([sub, data[sub], avg[sub], std[sub], z_score])
        # 計算各組的得分結果
        sum_a += z_score * float(linear_a[sub])
        sum_b += z_score * float(linear_b[sub])
        sum_c += z_score * float(linear_c[sub])
    # 加上方程式截距
    sum_a += float(linear_a[predict_cols])
    sum_b += float(linear_b[predict_cols])
    sum_c += float(linear_c[predict_cols])

    return person_grade, sum_a, sum_b, sum_c


def get_model(data):
    # 建立資料庫連線
    conn = sqlite3.connect(database)
    # 以 row 方式讀取，可以把資料以字典方式讀取近來
    conn.row_factory = sqlite3.Row
    # 查詢指定入學年、班級、類型=AVG，也就是查詢平均成績
    select_table = f"select * from score where {grade_cols} = {data[grade_cols]} " \
                   f"and {cls_cols} = {data[cls_cols]} " \
                   f"and {type_cols} = '{type_values[0]}'"
    # 執行查詢
    result = conn.execute(select_table)
    # 將結果以字典方式儲存
    average = dict(result.fetchone())
    # 查詢指定入學年、班級、類型=STDEV，也就是查詢標準差
    select_table = f"select * from score where {grade_cols} = {data[grade_cols]} " \
                   f"and {cls_cols} = {data[cls_cols]} " \
                   f"and {type_cols} = '{type_values[1]}'"
    result = conn.execute(select_table)
    stdev = dict(result.fetchone())
    # 查詢指定入學年、班級、類型=LINEAR_A，也就是查詢電力組線性迴歸式
    select_table = f"select * from score where {type_cols} = '{type_values[2]}'"
    # 執行查詢
    result = conn.execute(select_table)
    # 將結果以字典方式儲存
    linear_a = dict(result.fetchone())
    # 查詢指定入學年、班級、類型=LINEAR_B，也就是查詢控制組線性迴歸式
    select_table = f"select * from score where {type_cols} = '{type_values[3]}'"
    # 執行查詢
    result = conn.execute(select_table)
    # 將結果以字典方式儲存
    linear_b = dict(result.fetchone())
    # 查詢指定入學年、班級、類型=LINEAR_C，也就是查詢資通組線性迴歸式
    select_table = f"select * from score where {type_cols} = '{type_values[4]}'"
    # 執行查詢
    result = conn.execute(select_table)
    # 將結果以字典方式儲存
    linear_c = dict(result.fetchone())
    # 提交資料庫
    conn.commit()
    # 關閉資料庫連線
    conn.close()

    return average, stdev, linear_a, linear_b, linear_c


if __name__ == "__main__":
    init()
