from abc import ABC


# 只能被继承 不能实例化
class Tree(object, metaclass=ABC):
    class Position:
        """ 节点位置 """

        def element(self):
            """ 节点的内容"""
            raise NotImplementedError("必须由子类继承使用")

        def __eq__(self, other):
            """ 与节点是否一致 """
            raise NotImplementedError("必须由子类继承使用")

        def __ne__(self, other):
            """ 与节点是否不一致 """
            raise NotImplementedError("必须由子类继承使用")

    def root(self):
        """ 返回根节点 """
        raise NotImplementedError("必须由子类继承使用")

    def parent(self, p):
        """ 返回p的父节点 """
        raise NotImplementedError("必须由子类继承使用")

    def num_children(self, p):
        """ 返回p的子节点数量 """
        raise NotImplementedError("必须由子类继承使用")

    def children(self, p):
        """ 返回p的全部孩子节点 """
        raise NotImplementedError("必须由子类继承使用")

    def __len__(self):
        raise NotImplementedError("必须由子类继承使用")

    def is_root(self, p):
        return self.root() == p

    def is_leaf(self, p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, p):
        """ 返回p在树中的深度 """
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))


class BinaryTree(Tree, ABC):

    def left(self, p):
        """ 返回p的左孩子 """
        raise NotImplementedError("必须由子类继承使用")

    def right(self, p):
        """ 返回p的右孩子 """
        raise NotImplementedError("必须由子类继承使用")

    def sibling(self, p):
        """ 返回p的兄弟节点 """
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)


class LinkedBinaryTree(BinaryTree, ABC):
    class _TreeNode(object):
        __slots__ = "data", "parent", "right", "left"

        def __init__(self, data, parent=None, right=None, left=None):
            self.data = data
            self.parent = parent
            self.right = right
            self.left = left

    class Position(BinaryTree.Position, ABC):
        __slots__ = "container", "node"

        def __init__(self, container, node):
            self.container = container
            self.node = node

        def element(self):
            return self.node.data

        def __eq__(self, other):
            return type(other) is type(self) and other.node is self.node

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("p 必须是 Position 类型")
        if p.container is not self:
            raise ValueError("p 不属于该容器")
        if p.node.parent is p.node:
            raise ValueError("p 不合法")
        return p.node

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def root(self):
        return self._make_position(self.root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node.right)

    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def _add_root(self, e):
        if self.root is not None:
            raise ValueError("根节点已存在")
        self.root = self._TreeNode(e)
        self.size += 1
        return self._make_position(self.root)

    def _add_left(self, p, e):
        node = self._validate(p)
        if node.left is not None:
            raise ValueError("左孩子已存在")
        node.left = self._TreeNode(e, node)
        self.size += 1
        return self._make_position(node.left)

    def _add_right(self, p, e):
        node = self._validate(p)
        if node.right is not None:
            raise ValueError("右孩子已存在")
        node.right = self._TreeNode(e, node)
        self.size += 1
        return self._make_position(node.right)

    def _replace(self, p, e):
        node = self._validate(p)
        old = node.data
        node.data = e
        return old

    def _delete(self, p):
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError("p 有2个孩子节点")
        child = node.left if node.left else node.right
        if child is not None:
            child.parent = node.parent
        if node is self.root:
            self.root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        node.parent = node
        self.size -= 1
        return node.data


