from tools import Tool
from utils import HistoryQueue

class BaseAgent:
    def __init__(self, model, tools:Tool, window_size=10, system_prompt=None) -> None:
        self.model = model
        self.tools = tools
        self.history = HistoryQueue()
        self.system_prompt = system_prompt


    def chat(self, prompt, tools=None, history=None, *args, **kwargs):
        return self.model.chat(
            prompt = prompt, 
            tools = tools, 
            history = history, 
            system_prompt = self.system_prompt, 
            *args, 
            **kwargs
        )
    

    def run(
            self, 
            prompt, 
            use_history=False, 
            use_tool_result=False, 
            return_messages=True,
            debug=False,
    ):
        tool_descriptions = self.tools.get_all_description()

        history = self.history if use_history else None

        response, messages = self.chat(prompt, tools=tool_descriptions, history=history)

        if isinstance(response, tuple):
            # observation
            name, arguments, tool_call_id = response
            if debug:
                print(f"agent will use tool: [{name}] with args: [{arguments}]")
                
            tool_result = self.tools.get_tool(name)(**arguments)

            function_call = messages.pop(-1)

            if not use_tool_result:
                response, messages = self.chat(prompt=f"工具调用结果为{tool_result}", history=messages, tools=tool_descriptions)
        
        self.history.extend(messages)
        
        return response, messages if return_messages else response
            

    def delete_tool(self, tool):
        self.tools.delete(tool)


    def clear_tools(self, tools):
        for tool in tools:
            self.delete_tool(tool)
    

    def clear(self):
        self.history = HistoryQueue()
