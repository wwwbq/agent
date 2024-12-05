import os
import json


class Reader:
    """
    class to read files
    """
    def read(self, file: list = None, ):
        if not isinstance(file, list):
            file = [file]

        return [self.read_file_content(doc) for doc in file]

    def read_file_content(self, file_path: str):
        _, file_extension = os.path.splitext(file_path)

        try:
            return getattr(self, 'read_' + file_extension[1:].lower())(file_path)
        except:
            raise ValueError(f"Unsupported file type {file_extension[1:].lower()} for reading")

    """
    def read_pdf(self, file_path: str):
        # 读取PDF文件
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            return text


    def read_markdown(self, file_path: str):
        # 读取Markdown文件
        with open(file_path, 'r', encoding='utf-8') as file:
            md_text = file.read()
            html_text = markdown.markdown(md_text)
            # 使用BeautifulSoup从HTML中提取纯文本
            soup = BeautifulSoup(html_text, 'html.parser')
            plain_text = soup.get_text()
            # 使用正则表达式移除网址链接
            text = re.sub(r'http\S+', '', plain_text) 
            return text
    """

    def read_txt(self, file_path: str):
        # 读取文本文件
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def read_jsonl(file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(json.loads(line))
        return data


class Saver:
    """
    class to save files
    """
    def save(self, content, save_path, open_mode='a'):
        _, file_extension = os.path.splitext(save_path)
        try:
            getattr(self, f"save_{file_extension[1:].lower()}")(content, save_path, open_mode)
        except:
            raise ValueError(f"Unsupported file type {file_extension[1:].lower()} for saving")

    def save_txt(self, content, save_path, open_mode='a'):
        with open(save_path, open_mode, encoding='utf-8') as file:
            file.write(content+'\n')

    def save_json(self, content, save_path, open_mode='a'):
        with open(save_path, open_mode, encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    def save_jsonl(self, content, save_path, open_mode='a'):
        with open(save_path, open_mode, encoding='utf-8') as file:
            for item in content:
                file.write(json.dumps(item, ensure_ascii=False) + '\n')


class FileEngine:
    reader = Reader()
    saver = Saver()
    supproted_file_types = ['txt', 'json', 'jsonl']

    def read(self, file_path):
        return self.reader.read(file_path)
    
    def save(self, content, save_path, open_mode='w'):
        self.saver.save(content, save_path, open_mode)
        print(f"Save file {save_path} successfully!")
        return f"Save file {save_path} successfully!"

    def write(self, content, save_path, open_mode='a'):
        self.saver.save(content, save_path, open_mode)
        print(f"Write to {save_path} successfully!")
        return f"Write to {save_path} successfully!"

    def smart_write(self, content, save_folder, open_mode='a', file_extension="txt", size_threshold=1024*1024*100):
        # 获取当前标签下所有相同类型（txt、json等）的文件
        files = [f for f in os.listdir(save_folder) if file_extension in f]
        num_files = max(1, len(files))

        # 获取当前待写入文件的文件名
        cur_file_name = f"{num_files}.{file_extension}"

        # 如果当前文件大小大于阈值，则创建新文件
        # os.path.getsize单位是B, 默认阈值是100MB
        if len(files) > 0 and os.path.getsize(os.path.join(save_folder, cur_file_name)) > size_threshold:
            cur_file_name = f"{num_files + 1}.{file_extension}"

        # 写入内容到最新的文件
        self.write(content, os.path.join(save_folder, cur_file_name), open_mode)

        return f"Write to {os.path.join(save_folder, cur_file_name)} successfully!"
     



if __name__ == "__main__":
    from ..tools.conclusion import write_conclusion_to_txt, read_conclusion_by_label

    test1 = "11111"
    test2 = "22222"
    test3 = "33333"
    label1 = "测试1"
    label2 = "测试2"

    root = "./"

    write_conclusion_to_txt(test1, label1, root)
    write_conclusion_to_txt(test2, label2, root)
    write_conclusion_to_txt(test3, [label1, label2], root)
    # write_conclusion_to_txt(test1, root=root)
    # write_conclusion_to_txt(test1, root=root, file_name="test.txt")
    # write_conclusion_to_txt(test1, [label1, label2], root, file_name="test2.txt")
    results = read_conclusion_by_label(root, label1)

    print(1)
