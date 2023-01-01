# 从文件中转换到json的自定义类型
import json
from models import custom_encoder


def json_file_to_model(path: str, convert_type=object, json_txt_encoding='utf-8') -> object:
    with open(path, 'r') as f:
        r = json.load(f)
        # print(type(r))
        s = convert_type.from_dict(r)
    return s


# 从自定义类型转换到json文件
def model_to_json_file(export_path: str, json_txt_encoding='utf-8', src_object=object):
    with open(export_path, 'w', encoding=json_txt_encoding) as f:
        json.dump(src_object, f, ensure_ascii=False, cls=custom_encoder.CustomEncoder)
