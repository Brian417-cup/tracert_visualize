import json
from models import root, custom_encoder
from models import json_util

'''
总结:json文件->(自定义)实体类型：1.json.load(文件指针) 返回的是dict类型; 
                                 2.用dict恢复到(自定义)实体类型
     (自定义)实体类型->json文件  1.先自定义类MyCustomEncoder继承json.JSONEncoder，重写里面的default方法，其中:
                                   (1)如果是自定义实体类型调用默认的__dict__方法转换为dict类型；
                                   (2)如果是内置类型，调用json.JSONEncoder.default(self, 内置类型对象)方法即可;
                                 2.将转换后的dict类型用json.dump((自定义)实体类型,文件指针,
                                 ensure_ascii=False(为了防止中文无法正确被写入),cls=MyCustomEncoder类)
'''
# 这里模拟一个场景:对图这个数据结构进行一系列操作，最后再保存为json文件
if __name__ == '__main__':
    # 从json文件->恢复为自定义类型
    res = json_util.json_file_to_model(path='app.json', convert_type=root.Root)
    # 从自定义类型->json文件
    json_util.model_to_json_file(export_path='app2.json', src_object=res)
