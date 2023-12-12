

import pandas as pd
from json import dumps, loads


def search_in_table(tar_table :pd.DataFrame, col_name :str, input_info :str) -> None:
    return tar_table.loc[tar_table[col_name] == input_info]

def create_table(default_info :dict) -> pd.DataFrame:
    return pd.DataFrame(default_info)

def add_row_to_table(tar_table :pd.DataFrame, input_info :dict) -> None:
    tar_table.loc[len(tar_table)] = input_info

def delete_row_from_table() -> None:
    pass

def save_table() -> None:
    pass


default_header = {"task_name":[], "task_id":[], "assignee":[], "entity_id":[]}
table = create_table(default_header)
print(table)

assignee = [{"name":"송태영"}]
assignee_str = dumps(assignee)

input_infos = [
                {"task_name":"fx01", "task_id":123, "assignee":assignee_str, "entity_id":456},
                {"task_name":"fx02", "task_id":111, "assignee":assignee_str, "entity_id":333},
                {"task_name":"fx03", "task_id":122, "assignee":assignee_str, "entity_id":555},
               ]
for _info in input_infos:
    add_row_to_table(table, _info)

print(table)

res = search_in_table(table, "task_id", 123)
print(res)
print(res.iloc[0]["assignee"])
print(loads(res.iloc[0]["assignee"]))
print(res.to_dict("index"))
print(res.to_dict(orient='records'))



# # 한개의 column
# print(table["task_name"] )

# # 선택한 column 들
# print(table[["task_name", "entity_id"]] )


# # 한개의 row
# print(table.loc[[1]] )

# # 선택한 row들
# print(table.loc[[0,2]])


# Selection and Indexing Dataframe

# access cell

# Search by condition