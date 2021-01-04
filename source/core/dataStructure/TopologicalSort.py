from collections import defaultdict


class Node:
    def __init__(self, data=None):
        self.data = data
        self.in_degree = list()


class AOVNet:
    def __init__(self):
        self.__nodes_dict = defaultdict()

    def copy(self):
        ret = AOVNet()
        ret.__nodes_dict = self.__nodes_dict
        return ret

    def insert(self, _id, node):
        self.__nodes_dict[_id] = node

    def add_in_degree(self, _id_root, _id_in_degree):
        if _id_root == _id_in_degree:
            return
        if _id_root not in self.__nodes_dict.keys():
            return
        if _id_in_degree not in self.__nodes_dict.keys():
            return
        self.__nodes_dict[_id_root].in_degree.append(self.__nodes_dict[_id_in_degree])

    def remove(self, _id):
        the_node = self.__nodes_dict[_id]
        self.__nodes_dict.pop(_id)
        for node in self.__nodes_dict.values():
            for n in node.in_degree:
                if n == the_node:
                    node.in_degree.remove(the_node)

    def len(self):
        return len(self.__nodes_dict.keys())

    def get_O_in_degree_items(self):
        res_list = list()
        for item in self.__nodes_dict.items():
            if len(item[1].in_degree) == 0:
                res_list.append(item)
        return res_list


def topologicalSort(_AOVNet):
    if not isinstance(_AOVNet, AOVNet):
        return
    if _AOVNet.len() == 0:
        return
    res_list = list()
    while _AOVNet.len() > 0:
        O_list = _AOVNet.get_O_in_degree_items()
        while len(O_list) > 0:
            the_item = O_list.pop()
            res_list.append(the_item[1])  # 测试时可以改为0，以id看结果
            _AOVNet.remove(the_item[0])
    return res_list


# aovnet = AOVNet()
#
# aovnet.insert(0, Node())
# aovnet.insert(1, Node())
# aovnet.insert(2, Node())
# aovnet.insert(3, Node())
# aovnet.insert(4, Node())
# aovnet.insert(5, Node())
# aovnet.insert(6, Node())
#
# aovnet.add_in_degree(2, 0)
# aovnet.add_in_degree(6, 2)
# aovnet.add_in_degree(5, 2)
# aovnet.add_in_degree(3, 1)
# aovnet.add_in_degree(3, 2)
# aovnet.add_in_degree(4, 3)
# aovnet.add_in_degree(5, 4)
#
# print((topologicalSort(aovnet.copy())))
