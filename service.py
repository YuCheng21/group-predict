import sqlite3
import os
import train

MODEL = [[1, 103, 1, 'AVG', 64.0851, 58.0213, 68.0638, 64.9787, 62.6383, 75.4468, 79.0638, 64.4681, 71.1489, 69.4255, 70.5319, 83.4681, 0.0], [2, 103, 1, 'STDEV', 11.2719, 13.874, 9.8443, 10.3769, 8.8352, 9.7015, 6.9325, 10.9444, 7.6991, 8.9341, 7.1425, 2.7121, 0.0], [3, 103, 2, 'AVG', 62.94, 59.1, 71.96, 63.26, 69.4, 59.8, 84.44, 70.68, 66.68, 63.58, 68.46, 84.38, 0.0], [4, 103, 2, 'STDEV', 14.4242, 22.1181, 9.239, 16.1565, 10.3885, 20.1623, 4.1287, 8.3077, 7.8318, 14.5273, 12.8284, 2.7921, 0.0], [5, 103, 3, 'AVG', 62.898, 58.2857, 74.102, 70.7143, 62.2041, 66.1429, 82.8367, 67.7551, 67.2449, 52.8776, 85.0408, 78.8163, 0.0], [6, 103, 3, 'STDEV', 13.1293, 19.7804, 15.3825, 17.5987, 11.425, 12.289, 5.0116, 9.144, 9.488, 13.7924, 8.7481, 6.7783, 0.0], [7, 104, 1, 'AVG', 60.902, 57.3529, 58.1961, 72.1373, 60.3333, 72.098, 83.7647, 64.7059, 68.451, 65.451, 63.3333, 84.2549, 0.0], [8, 104, 1, 'STDEV', 14.4076, 20.7088, 17.5756, 14.6529, 19.2361, 11.3677, 5.5008, 11.354, 13.8384, 8.8767, 10.1666, 3.086, 0.0], [9, 104, 2, 'AVG', 63.3778, 57.8222, 67.1111, 63.2, 61.7333, 74.1778, 81.6667, 64.8889, 68.2222, 65.6444, 64.4, 80.7333, 0.0], [10, 104, 2, 'STDEV', 10.8552, 17.048, 13.2484, 16.3239, 15.9491, 13.3538, 7.4147, 14.8836, 11.3644, 14.4224, 15.0619, 5.7403, 0.0], [11, 104, 3, 'AVG', 63.3617, 62.0213, 70.2128, 68.5106, 72.2128, 70.3617, 84.9787, 70.1915, 65.2553, 43.5319, 82.8298, 70.7021, 0.0], [12, 104, 3, 'STDEV', 19.7456, 23.2035, 21.7852, 21.1679, 13.9527, 12.0043, 6.8401, 10.6264, 17.6255, 26.4783, 14.9001, 10.2395, 0.0], [13, 0, 0, 'LINEAR_A', -0.139139, 0.194754, 0.204601, -0.110807, -0.231601, 0.227877, 0.158745, 0.041444, -0.127191, 0.001311, 0.159636, 0.274198, -0.157744], [14, 0, 0, 'LINEAR_B', 0.0188, -0.020718, 0.05001, 0.076795, 0.102582, 0.035617, 0.083496, 0.083288, -0.142996, 0.145437, 0.200214, -0.059279, 0.084213], [15, 0, 0, 'LINEAR_C', 0.258979, -0.388678, 0.126887, 0.157012, -0.039246, -0.113958, 0.077287, -0.170431, 0.132618, 0.154188, 0.299535, 0.010626, 0.028152]]

current_path = os.path.dirname(__file__)
database = current_path + "/database.sqlite"

id_cols = "ID"
type_cols = "??????"

cls_cols = train.cls_cols
grade_cols = train.grade_cols
# output = 1 ???
predict_cols = train.predict_cols
# input = 13 ???
subject_cols = train.subject_cols
# ???????????????????????? ????????????????????????????????????????????????????????????????????????????????????
type_values = train.type_values


def init():
    # ?????????????????????
    conn = sqlite3.connect(database)
    # ?????????????????????????????????????????????
    delete_table = f"drop table if exists score"
    # ????????????
    conn.execute(delete_table)
    # ??????????????????????????????????????????????????????????????????????????????????????????
    create_table = f"create table if not exists score (" \
                   f"'{id_cols}' int not null, '{grade_cols}' int default null, " \
                   f"'{cls_cols}' int default null, '{type_cols}' varchar default null, "
    # ????????????????????????????????????????????????
    for sub in subject_cols:
        create_table += f"'{sub}' float default null, "
    # ???????????????????????????????????????
    create_table += f"'{predict_cols}' float default null)"
    # ????????????
    conn.execute(create_table)
    # ?????????????????????????????????????????????
    for model_col in MODEL:
        # ????????????????????????????????????????????????????????????
        insert_data = f"insert into score ('{id_cols}', '{grade_cols}', '{cls_cols}', '{type_cols}', "
        # ??????????????????????????????????????????
        for sub in subject_cols:
            insert_data += f"'{sub}', "
        # ??????????????????????????????????????????
        insert_data += f"'{predict_cols}') values ("
        # ????????????????????????????????????????????????
        for index, models in enumerate(model_col):
            # ?????????????????????????????????
            if index == 3:
                insert_data += f", '{models}'"
            # ?????? >0 ?????????????????????
            elif index:
                insert_data += f", {models}"
            # ?????? =0 ???????????????
            else:
                insert_data += f"{models}"
        # ?????????????????????
        insert_data += f")"
        # ????????????
        conn.execute(insert_data)
    # ???????????????
    conn.commit()
    # ?????????????????????
    conn.close()


def predict(data):
    # ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    avg, std, linear_a, linear_b, linear_c = get_model(data)
    # ????????????????????????
    sum_a, sum_b, sum_c = 0, 0, 0
    # ????????????????????????????????????
    person_grade = []
    # ????????????????????????????????????????????????????????????????????????????????? (y=ax+b)
    for sub_index, sub in enumerate(subject_cols):
        # ?????????????????????(???????????? - ?????????) / ????????? = ???????????? (Z-Score)
        z_score = (float(data[sub]) - float(avg[sub])) / float(std[sub])
        # ?????????????????????????????????????????????????????????????????????????????????????????????
        person_grade.append([sub, data[sub], avg[sub], std[sub], z_score])
        # ???????????????????????????
        sum_a += z_score * float(linear_a[sub])
        sum_b += z_score * float(linear_b[sub])
        sum_c += z_score * float(linear_c[sub])
    # ?????????????????????
    sum_a += float(linear_a[predict_cols])
    sum_b += float(linear_b[predict_cols])
    sum_c += float(linear_c[predict_cols])

    return person_grade, sum_a, sum_b, sum_c


def get_model(data):
    # ?????????????????????
    conn = sqlite3.connect(database)
    # ??? row ?????????????????????????????????????????????????????????
    conn.row_factory = sqlite3.Row
    # ???????????????????????????????????????=AVG??????????????????????????????
    select_table = f"select * from score where {grade_cols} = {data[grade_cols]} " \
                   f"and {cls_cols} = {data[cls_cols]} " \
                   f"and {type_cols} = '{type_values[0]}'"
    # ????????????
    result = conn.execute(select_table)
    # ??????????????????????????????
    average = dict(result.fetchone())
    # ???????????????????????????????????????=STDEV???????????????????????????
    select_table = f"select * from score where {grade_cols} = {data[grade_cols]} " \
                   f"and {cls_cols} = {data[cls_cols]} " \
                   f"and {type_cols} = '{type_values[1]}'"
    result = conn.execute(select_table)
    stdev = dict(result.fetchone())
    # ???????????????????????????????????????=LINEAR_A??????????????????????????????????????????
    select_table = f"select * from score where {type_cols} = '{type_values[2]}'"
    # ????????????
    result = conn.execute(select_table)
    # ??????????????????????????????
    linear_a = dict(result.fetchone())
    # ???????????????????????????????????????=LINEAR_B??????????????????????????????????????????
    select_table = f"select * from score where {type_cols} = '{type_values[3]}'"
    # ????????????
    result = conn.execute(select_table)
    # ??????????????????????????????
    linear_b = dict(result.fetchone())
    # ???????????????????????????????????????=LINEAR_C??????????????????????????????????????????
    select_table = f"select * from score where {type_cols} = '{type_values[4]}'"
    # ????????????
    result = conn.execute(select_table)
    # ??????????????????????????????
    linear_c = dict(result.fetchone())
    # ???????????????
    conn.commit()
    # ?????????????????????
    conn.close()

    return average, stdev, linear_a, linear_b, linear_c


if __name__ == "__main__":
    init()
