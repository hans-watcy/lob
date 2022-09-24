import time

class Level:
    def __init__(self, price, size, time):
        self.price = price
        self.size = size
        self.time = time

class node:
    def __init__(self, level):
        self.value = level
        self.left = None
        self.right = None
        self.height = 1

class AVL:

    def height(self, Node):
        if Node is None:
            return 0
        else:
            return Node.height

    def balance(self, Node):
        if Node is None:
            return 0
        else:
            return self.height(Node.left) - self.height(Node.right)

    def MinimumValueNode(self, Node):
        if Node is None or Node.left is None:
            return Node
        else:
            return self.MinimumValueNode(Node.left)

    def rotateR(self, Node):
        a = Node.left
        b = a.right
        a.right = Node
        Node.left = b
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
        a.height = 1 + max(self.height(a.left), self.height(a.right))
        return a

    def rotateL(self, Node):
        a = Node.right
        b = a.left
        a.left = Node
        Node.right = b
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
        a.height = 1 + max(self.height(a.left), self.height(a.right))
        return a

    def insert(self, level, root):
        if root is None:
            return node(level)
        elif level.price == root.value.price:
            root.value = level
        elif level.price < root.value.price:
            root.left = self.insert(level, root.left)
        elif level.price > root.value.price:
            root.right = self.insert(level, root.right)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)
        if balance > 1 and root.left.value.price > level.price:
            return self.rotateR(root)
        if balance < -1 and level.price > root.right.value.price:
            return self.rotateL(root)
        if balance > 1 and level.price > root.left.value.price:
            root.left = self.rotateL(root.left)
            return self.rotateR(root)
        if balance < -1 and level.price < root.right.value.price:
            root.right = self.rotateR(root.right)
            return self.rotateL(root)
        return root

    def preorder(self, root):
        if root is None:
            return
        print(root.value.price, root.value.size, root.value.time)
        self.preorder(root.left)
        self.preorder(root.right)

    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.value)
            res = res + self.inorderTraversal(root.right)
        return res

    def delete(self, level, Node):
        if Node is None:
            return Node
        elif level.price < Node.value.price:
            Node.left = self.delete(level, Node.left)
        elif level.price > Node.value.price:
            Node.right = self.delete(level, Node.right)
        else:
            if Node.left is None:
                lt = Node.right
                Node = None
                return lt
            elif Node.right is None:
                lt = Node.left
                Node = None
                return lt
            rgt = self.MinimumValueNode(Node.right)
            Node.value = rgt.value
            Node.right = self.delete(rgt.value, Node.right)
        if Node is None:
            return Node
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
        balance = self.balance(Node)
        if balance > 1 and self.balance(Node.left) >= 0:
            return self.rotateR(Node)
        if balance < -1 and self.balance(Node.right) <= 0:
            return self.rotateL(Node)
        if balance > 1 and self.balance(Node.left) < 0:
            Node.left = self.rotateL(Node.left)
            return self.rotateR(Node)
        if balance < -1 and self.balance(Node.right) > 0:
            Node.right = self.rotateR(Node.right)
            return self.rotateL(Node)
        return Node


if __name__=='__main__':
    order = Level(1,1,1)
    Tree = AVL()
    rt = None
    rt = Tree.insert(order, rt)
    order = Level(2, 2, 2)
    rt = Tree.insert(order, rt)
    print(Tree.preorder(rt))

    rt = Tree.delete(order, rt)

    print(Tree.preorder(rt))
