import asyncio
import inspect
from livekit.agents import function_tool

def make_dynamic_tool(name, desc, properties, required):
    parameters = []
    for prop_name, prop_type in properties.items():
        annotation = str
        if prop_type == "integer": annotation = int
        elif prop_type == "boolean": annotation = bool
        
        default = inspect.Parameter.empty if prop_name in required else None
        
        param = inspect.Parameter(
            name=prop_name,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default,
            annotation=annotation
        )
        parameters.append(param)
        
    async def dynamic_func(**kwargs):
        return f"Called {name} with {kwargs}"
        
    dynamic_func.__name__ = name
    dynamic_func.__doc__ = desc
    dynamic_func.__signature__ = inspect.Signature(parameters=parameters, return_annotation=str)  # type: ignore
    
    # Try decorating it
    decorated = function_tool(dynamic_func)
    return decorated

tool = make_dynamic_tool("test_tool", "A test tool", {"x": "integer", "y": "integer"}, ["x", "y"])
print(f"Tool Name: {tool.name}")
print(f"Tool Desc: {tool.description}")
print(f"Tool Args: {tool.arg_info}")
