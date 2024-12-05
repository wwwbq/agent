from utils import Registry


class Tool(Registry):
    def register(self, obj=None, description=None):
        if obj is None:
            # used as a decorator
            def deco(func_or_class):
                name = func_or_class.__name__
                self._do_register(name, {"tool": func_or_class, "description": description})
                return func_or_class

            return deco

        # used as a function call
        name = obj.__name__
        self._do_register(name, {"tool": obj, "description": description})

    def get_tool(self, tool):
        return self.get(tool)["tool"]
    
    def get_description(self, tool):
        return self.get(tool)["description"]
    
    def get_all_description(self):
        return [self.get_description(tool) for tool in self._obj_map]
    
    def delete(self, tool):
        if not isinstance(tool):
            tool = tool.__name__
        self._obj_map.pop(tool)
    
tools = Tool()