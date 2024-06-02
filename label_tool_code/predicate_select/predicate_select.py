import json
import openpyxl

caption_path1 = 'E:/专业学习/数据集/Sydney_captions/dataset.json'
caption_path2 = 'E:/专业学习/数据集/UCM_captions/dataset.json'
caption_path3 = 'E:/专业学习/数据集/RSICD/annotations_rsicd/dataset_rsicd.json'

total_word = []
data = json.load(open(caption_path1))

all_word1 = []
for img_id in range(len(data['images'])):
    # print(data['images'][img_id]['filename'])
    word1 = []
    for i, ele in enumerate(data["images"][img_id]['sentences']):
        # print(ele['raw'])
        word1.extend(ele['tokens'])
    # print(list(set(word)))
    all_word1.extend(list(set(word1)))
total_word.extend(list(set(all_word1)))
print(len(list(set(all_word1))))


data = json.load(open(caption_path2))

all_word2 = []
for img_id in range(len(data['images'])):
    # print(data['images'][img_id]['filename'])
    word2 = []
    for i, ele in enumerate(data["images"][img_id]['sentences']):
        # print(ele['raw'])
        word2.extend(ele['tokens'])
    # print(list(set(word)))
    all_word2.extend(list(set(word2)))
total_word.extend(list(set(all_word2)))
print(len(list(set(all_word2))))


data = json.load(open(caption_path3))

all_word3 = []
for img_id in range(len(data['images'])):
    # print(data['images'][img_id]['filename'])
    word3 = []
    for i, ele in enumerate(data["images"][img_id]['sentences']):
        # print(ele['raw'])
        word3.extend(ele['tokens'])
    # print(list(set(word)))
    all_word3.extend(list(set(word3)))
total_word.extend(list(set(all_word3)))
print(len(list(set(all_word3))))

print(len(list(set(total_word))))
print(list(set(total_word)))


def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        # for j in range(0, len(value[i])):
        sheet.cell(row=i + 1, column=1, value=value[i])
    workbook.save(path)
    print("xlsx格式表格写入数据成功！")


book_name_xlsx = 'caption word.xlsx'

sheet_name_xlsx = 'caption word'

value3 = list(set(total_word))

write_excel_xlsx(book_name_xlsx, sheet_name_xlsx, value3)
