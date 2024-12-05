from agents import BaseAgent
from models import APIModel
from tools import tools

system_prompt = "你是AI小助手Cookiee，在回答问题时你会优先调用工具来获得结果，没有工具调用你才会根据自己的知识进行回答，如果用户告诉你工具调用的返回值，请你自己组织语言告诉用户工具调用的结果"

model = APIModel()

agent = BaseAgent(model=model, tools=tools, system_prompt=system_prompt)

prompt = "请帮我记录一下：attention可以用在视觉任务中，标签为NLP"
prompt2 = "帮我查阅一下NLP标签下有些什么记录"

response, messages = agent.run(prompt)
print(response)

response, messages = agent.run(prompt2)
print(response)