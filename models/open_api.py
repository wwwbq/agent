from openai import OpenAI
import json

#peTI7xndTJ9zpgXOF6xogYQIA2umfYRK

API_KEY = "XXX"
MODEL_ID = "XXX"

class APIModel:
    def __init__(self, model=MODEL_ID, api_key=API_KEY, client=None,) -> None:
        if client is None:
            self.client = OpenAI(
                api_key = api_key,
                base_url = "https://ark.cn-beijing.volces.com/api/v3",
            )
        else:
            self.client = client

        self.model = model
    
    def chat(
            self,
            prompt, 
            system_prompt=None, 
            tools=None, 
            history=None, 
            return_messages=True,
    ):
        messages = [{"role": "user", "content": prompt}]
    
        if history is not None:
            messages = history + messages
        
        if system_prompt:
            if len(messages) > 0 and messages[0]["role"] != "system":
                messages.insert(0, {"role": "system", "content": system_prompt})
            elif len(messages) == 0:
                messages.append({"role": "system", "content": system_prompt})

        completion = self.client.chat.completions.create(
            model = self.model, 
            messages = messages,
            tools = tools,
        )

        role = completion.choices[0].message.role
        response = completion.choices[0].message.content
        tool_call = completion.choices[0].message.tool_calls

        if return_messages:
            if tool_call:
                name, arguments = tool_call[0].function.name, json.loads(tool_call[0].function.arguments)
                tool_call_id = tool_call[0].id
                messages.append({"role": "function", "content": json.dumps({"name": name, "argument": arguments}, ensure_ascii=False), "tool_call_id": tool_call_id})
                response = (name, arguments, tool_call_id)
            else:
                messages.append({"role": role, "content": response})
            return response, messages
        
        else:
            if tool_call:
                response = (name, arguments)
            return response


def chat(
    prompt=None, 
    api_key=API_KEY,
    model_id=MODEL_ID,
    client=None,
    system_prompt=None, 
    tools=None,
    history=None, 
    return_messages=True,
    *args,
    **kwargs,
) -> None:

    if client is None:
        client = OpenAI(
            api_key = api_key,
            base_url = "https://ark.cn-beijing.volces.com/api/v3",
        )

    messages = [{"role": "user", "content": prompt}]
    
    if history is not None:
        messages = history.extend(messages)
    
    if system_prompt:
        if len(messages) > 0 and messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": system_prompt})
        elif len(messages) == 0:
            messages.append({"role": "system", "content": system_prompt})

    completion = client.chat.completions.create(
        model = model_id, 
        messages = messages,
        tools = tools,
    )

    role = completion.choices[0].message.role
    response = completion.choices[0].message.content
    tool_call = completion.choices[0].message.tool_calls

    if return_messages:
        if tool_call:
            name, arguments = tool_call[0].function.name, json.loads(tool_call[0].function.arguments)
            tool_call_id = tool_call[0].id
            messages.append({"role": "function", "content": json.dumps({"name": name, "argument": arguments}, ensure_ascii=False), "tool_call_id": tool_call_id})
            response = (name, arguments, tool_call_id)
        else:
            messages.append({"role": role, "content": response})
        return response, messages
    
    else:
        if tool_call:
            response = (name, arguments)
        return response
