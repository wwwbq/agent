from models.open_api import chat
from tools import tools

'''
tools = [
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
'''
    
# tool_map = {
#     "write_conclusion_to_txt": write_conclusion_to_txt,
#     "read_conclusion_by_label": read_conclusion_by_label,
# }

tool_descriptions = tools.get_all_description()

system_prompt = "你是AI小助手Cookiee，在回答问题时你会优先调用工具来获得结果，没有工具调用你才会根据自己的知识进行回答，如果用户告诉你工具调用的返回值，请你自己组织语言告诉用户工具调用的结果"

prompt = "请帮我记录一下我对attnetion is all you need这篇论文总结：表明了attention的重要性，以后应该可以用在其他任务中。标签就设置为NLP吧"

response, messages = chat(prompt, tools=tool_descriptions, system_prompt=system_prompt)

print(response)
print(messages)

if isinstance(response, tuple):
    # observation
    name, arguments, tool_call_id = response
    #tool_result = tool_map[name](**arguments)
    tool_result = tools.get_tool(name)(**arguments)
    function_call = messages.pop(-1)
    #messages.append({"role": "tool", "content": f"工具调用结果显示gpa为{tool_result}", "tool_call_id": tool_call_id, "name": name})
    messages.append({"role": "user", "content": f"工具调用结果显示gpa为{tool_result}"})
    response, messages = chat(history=messages, tools=tools)

print(response)
print(messages)