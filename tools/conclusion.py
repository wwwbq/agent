import os
from .base_tool import tools
from utils.file import FileEngine


engine = FileEngine()

descriptions = [
        {
            "type": "function",
            "function": {
                "name": "write_conclusion_to_txt",
                "description": "当用户记录某些内容（通常是对某些知识的总结）时，保存其到本地的txt中",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "用户上传的所总结的内容"},
                        "labels": {"type": "array", "items": {"type": "string"}, "description": "总结内容对应的标签"},
                        "root": {"type": "string", "description": "保存路径"},
                        "file_name": {"type": "string", "description": "保存的文件名"},
                    },
                    "required": ["content",],
                },
            },
        },
         {
            "type": "function",
            "function": {
                "name": "read_conclusion_by_label",
                "description": "根据指定的标签读取知识库里对应标签的内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string",  "description": "所指定的标签"},
                        "root": {"type": "string",  "description": "知识库在本地的路径"},
                    },
                    "required": ["label", ],
                },
            },
        },
    ]


# 输入root路径和标签，在root路径下创建对应标签的文件夹
#@tools.register()
def get_label_folder(root, label):
    if label in [None, ""]:
        label = "通用"

    label_path = os.path.join(root, label)

    if not os.path.exists(label_path):
        os.makedirs(label_path, exist_ok=True)
        print(f"Create folder {label_path} successfully!")

    return label_path


# 输入一段总结和对应的标签，根据标签创建txt文件，然后将总结追加到此txt中
@tools.register(description=descriptions[0])
def write_conclusion_to_txt(content, labels=None, root="./save", file_name=None):
    if labels is None:
        labels = [""]

    if not isinstance(labels, list):
        labels = [labels]

    # 某段内容可能对应多个标签
    for label in labels:
        file_path = get_label_folder(root, label)

        if file_name is None:
            return engine.smart_write(content, file_path)
        else:
            return engine.write(content, os.path.join(file_path, file_name))


# 根据标签查找所有的总结
@tools.register(description=descriptions[1])
def read_conclusion_by_label(label, root="./save", return_str=False):

    folder = get_label_folder(root, label)
    files = [os.path.join(folder, f) for f in os.listdir(folder)]

    return engine.read(files) if not return_str else "".join(engine.read(files))

