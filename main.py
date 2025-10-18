from random import random


class Node:

    def __init__(self, value: int):
        self.value = value
        self.priority = random()
        self.size = 1
        self.sum = value
        self.left, self.right = None, None
    

class Treap:
    def __init__(self, values: [int]=None):
        self.root = None
        if values:
            for n in values:
                self.root = self.merge(self.root, Node(n)) #  147

                    
    def update(self, node: Node):
        if node:
            if node.right:
                r_size = node.right.size
                r_sum = node.right.sum
            else:
                r_size = 0
                r_sum = 0
            if node.left:
                l_size = node.left.size
                l_sum = node.left.sum
            else:
                l_size = 0
                l_sum = 0
            node.sum = r_sum + l_sum + node.value
            node.size = r_size + l_size + 1

            
    def split_by_size(self, node: Node, k: int) -> (Node, Node): #  139
        if not node:
            return (None, None)

        left_size = node.left.size if node.left else 0

        if k <= left_size:
            LL, LR = self.split_by_size(node.left, k)
            node.left = LR
            self.update(node)
            return LL, node
        else:
            RL, RR = self.split_by_size(node.right, k - left_size - 1)
            node.right = RL
            self.update(node)
            return node, RR


    def merge(self, left: Node, right: Node) -> Node:
        if not left:
            return right
        if not right:
            return left
        if left.priority > right.priority:
            left.right = self.merge(left.right, right)
            self.update(left)
            return left
        else:
            right.left = self.merge(left, right.left)
            self.update(right)
            return right


    def sum(self, from_index: int, to_index: int) -> int: #  153
        if from_index > to_index or not self.root or from_index < 0 or to_index >= self.root.size:
            raise ValueError
        L, R = self.split_by_size(self.root, from_index)
        RL, RR = self.split_by_size(R, to_index - from_index + 1)
        res = RL.sum
        self.root = self.merge(L, self.merge(RL, RR))
        return res


    def insert(self, pos, val):
        if pos < 0 or pos > (self.root.size if self.root else 0):
            raise ValueError

        new_node = Node(val)
        if not self.root:
            self.root = new_node
        else:
            L, R = self.split_by_size(self.root, pos)
            self.root = self.merge(self.merge(l, new_node), R)


    def erase(self, pos, count=None):
        if not count:
            if pos < 0 or pos >= (self.root.size if self.root else 0):
                raise ValueError
    
            L, T = self.split_by_size(self.root, pos)
            TL, TR = self.split_by_size(T, 1)
            self.root = self.merge(L, TR)
        else:
            if pos < 0 or pos > (self.root.size if self.root else 0):
                raise ValueError

            L, T = self.split_by_size(self.root, pos)
            TL, TR = self.split_by_size(T, count)
            self.root = self.merge(L, TR)


def test1():
    arr = list(range(1, 208, 7))
    t = Treap(arr)
    assert t.sum(4, 11) == sum(arr[4:12])

def test2():
    arr = [42]
    t = Treap(arr)
    assert t.sum(0, 0) == 42

def test3():
    arr = list(range(5, 126, 5))
    t = Treap(arr)
    assert t.sum(len(arr) - 1, len(arr) - 1) == arr[-1]

def test4():
    arr = list(range(12, 487, 13))
    t = Treap(arr)
    assert t.sum(0, 0) == arr[0]

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    

