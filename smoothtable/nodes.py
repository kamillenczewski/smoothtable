from typing import Iterable

class Node:
    def __init__(self, data):
        self.higherNode: Node = None
        self.lowerNodes: list[Node] = []
        self.data = data

    def _connectLower(self, node):
        self.lowerNodes.append(node)

    def _connectHigher(self, node):
        self.higherNode = node

    def connectLower(self, node: 'Node'):
        self._connectLower(node)
        node._connectHigher(self)
        return self

    def connectHigher(self, node: 'Node'):
        self._connectHigher(node)
        node._connectLower(self)
        return self
    
    def connectManyLower(self, *nodes):
        for node in nodes:
            if isinstance(node, Iterable):
                self.connectManyLower(*node)
            else:
                self.connectLower(node)
                
        return self