import json

with open("C:/Users/27165/Desktop/scene_graphs.json", 'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict[0]["objects"])