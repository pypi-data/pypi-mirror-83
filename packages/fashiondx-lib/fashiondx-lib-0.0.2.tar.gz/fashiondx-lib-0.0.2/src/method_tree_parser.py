from typing import Any, Callable, Dict, List, Tuple, Union

import pandas as pd


class InvalidMethodTree(Exception): pass


class MethodTree(object):
    def __init__(self, value: Any):
        self.value = value
        self.children = []
        self.parent = None

    def compute(self, data: pd.DataFrame, method_map: Dict[str, Callable],
                **kwargs) -> Any:
        if self.value["object"] == "direct":
            return self.value["variable"]
        elif self.value["object"] == "kwargs_obj":
            return kwargs[self.value["variable"]]
        elif self.value["object"] == "data_obj":
            return data[self.value["variable"]]
        elif self.value["object"] == "method":
            foo = method_map[self.value["variable"]]
            args = [
                child.compute(data, method_map, **kwargs)
                for child in self.children
            ]
            return foo(args)
        else:
            err = "Object type %s not recognised." % self.value["object"]
            raise InvalidMethodTree(err)


def parse(method_tree: List[Dict[str, str]]) -> MethodTree:
    children = method_tree.pop("children", [])
    root = MethodTree(method_tree)
    for child in children:
        node = parse(child)
        node.parent = root
        root.children.append(node)
    return root


# def parse(method_tree: List[Dict[str, str]]) -> MethodTree:
#     root = MethodTree(method_tree[0])
#     curr_node = root
#     stack = []
#     index = 1

#     while(index < len(method_tree)):
#         if method_tree[index] == "<":
#             stack.append("<")
#             node = MethodTree(method_tree[index + 1])
#             node.parent = curr_node
#             curr_node.children.append(node)
#             curr_node = node
#             index += 2
#         elif method_tree[index] == ">":
#             if not stack:
#                 raise InvalidMethodTree("Method tree is not balanced")
#             stack.pop()
#             curr_node = curr_node.parent
#             index += 1

#     if stack:
#         raise InvalidMethodTree("Method tree is not balanced")
#     return root
