import json
#
# # 准备json格式的字符串
# json_str = '{"a":10, "b":20, "c":true, "d":["a","b","中文"]}'
#
# # 把json字符串转为为python
# dic = json.loads(json_str)
# print(dic)
# # 把python中数据类型转换为json字符串
# json_s = json.dumps(dic, ensure_ascii=False)
# print(json_s)
#
# # 操作文件
# with open("test.json", 'w', encoding='utf8') as f:
#     json.dump(dic, f)
#
# # with open("test.json", 'w', encoding='utf8') as f:
# #   json.dump(dic, f, ensure_ascii=False, indent=2)


# json模块只能处理标准的json字符串
json_str = "{'a':1, 'b':2, 'c':3}"
#  报错
# dic = json.loads(json_str)
# print(dic)
# 方案1: 如果数量比较小,可以使用eval
dic = eval(json_str)
print(dic)
print(type(dic))

# 方案2: 把单引号,都替换为""
# json_str = json_str.replace("'", "\"")
json_str = json_str.replace("'", '"')
dic = json.loads(json_str)
print(dic)
