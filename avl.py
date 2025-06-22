from node import Node
from object import Color
from exceptions import *
def comp_1(key, value, node):
    if node.key < key:
        return -1
    elif node.key > key:
        return 1
    elif node.key == key:
        if node.value.bin_id < value.bin_id:
            return -1
        elif node.value.bin_id > value.bin_id:
            return 1
        else: return 0
def comp_2(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else: # node_1.key == node_2.key
        if node_1.value > node_2.value.bin_id:
            return 1
        elif node_1.value < node_2.value.bin_id:
            return -1
        else: return 0

class AVLTree:
    def __init__(self, compare_function = comp_1):
        self.root = None
        self.comparator = compare_function


    def height(self, node):
        if not node:
            return 0
        return node.height
    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))
    def isbalance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self.update_height(x)
        self.update_height(y)

        # Return the new root
        return y


    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self.update_height(y)
        self.update_height(x)

        # Return the new root
        return x



    def search_bin(self, key, color):
        if self.root is None:
            raise Exception
        if color == Color.BLUE:
            node1 = self._search_blue(self.root, key)
            if node1.key >= key:
                return node1
            else:
                raise Exception
        elif color == Color.GREEN:
            node2 = self._search_green(self.root, key)
            if node2.key >= key:
                return node2
            else:
                raise Exception
        elif color == Color.RED:
            node3 = self._search_green(self.root, key)
            cap = node3.key
            node4 = self._search_blue(self.root, cap)
            if node4.key >= key:
                return node4
            else:
                raise Exception
        elif color == Color.YELLOW:
            node2 = self._search_blue(self.root, key)
            min_cap = node2.key
            node5 = self._search_yellow(self.root, min_cap)
            if node5.key >= key:
                return node5
            else:
                raise Exception

    def _search_blue(self, root, key, candidate = None):
        if not root:
            if candidate is None:
                raise NoBinFoundException
            return candidate
        if root.key < key:
            return self._search_blue(root.right, key, candidate)
        if root.key >= key:
            if candidate is None or root.key <= candidate.key:
                candidate = root
            return self._search_blue(root.left, key, candidate)

    def _search_yellow(self, root, min_cap, candidate = None):
        if not root:
            return candidate
        if root.key > min_cap:
            return self._search_yellow(root.left, min_cap, candidate)
        if root.key < min_cap:
            return self._search_yellow(root.right, min_cap, candidate)
        else:
            if candidate is None or candidate.value.bin_id < root.value.bin_id:
                candidate = root
            return self._search_yellow(root.right, min_cap, candidate)

    def _search_green(self,root, key, candidate = None):
        if not root:
            if candidate is None:
                raise NoBinFoundException
            return candidate
        if root.key >= key:
            if candidate is None or root.key > candidate.key or (root.key == candidate.key and root.value.bin_id > candidate.value.bin_id):
                candidate = root
        return self._search_green(root.right, key, candidate)


    def search_object_bin_id(self, object_id):
        return self._search_obj(self.root, object_id)
    def _search_obj(self, root, object_id):
        if not root or root.key == object_id:
            return root
        if root.key > object_id:
            return self._search_obj(root.left, object_id)
        return self._search_obj(root.right, object_id)



    def insert_object(self, key, value):
        self.root = self._insert_obj(self.root, key, value)
    def _insert_obj(self, root, key, value):
        if not root:
            new_node = Node(key, value)
            return new_node
        elif key < root.key:
            root.left = self._insert_obj(root.left, key, value)
        else:
            root.right = self._insert_obj(root.right, key, value)
        self.update_height(root)
        balance = self.isbalance(root)

        # Left rotation
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        # Right rotation
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        # Left-Right rotation
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right-Left rotation
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def min_key_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current
    def delete_object(self, key):
        self.root = self._delete_obj(self.root, key)
    def _delete_obj(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self._delete_obj(root.left, key)
        elif key > root.key:
            root.right = self._delete_obj(root.right, key)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.min_key_node(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = self._delete_obj(root.right, temp.key)
        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.isbalance(root)

        # Left rotation
        if balance > 1 and self.isbalance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.isbalance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.isbalance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.isbalance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def insert_bin(self, key, value):
        self.root = self._insert_b(self.root, key, value)
    def _insert_b(self, root, key, value):
        if not root:
            new_node = Node(key, value)
            return new_node

        elif self.comparator(key, value, root) > 0:
            root.left = self._insert_b(root.left, key, value)
        elif self.comparator(key, value, root) < 0:
            root.right = self._insert_b(root.right, key, value)
        self.update_height(root)
        balance = self.isbalance(root)

        # Left rotation
        if balance > 1 and (key < root.left.key or (key == root.left.key and value.bin_id < root.left.value.bin_id)):
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and (key > root.right.key or (key == root.right.key and value.bin_id > root.right.value.bin_id)):
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and (key > root.left.key or (key == root.left.key and value.bin_id > root.left.value.bin_id)):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and (key < root.right.key or (key == root.right.key and value.bin_id < root.right.value.bin_id)):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete_bin(self, key, value):
        self.root = self._delete_b(self.root, key, value)
    def _delete_b(self, root, key, value):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete_b(root.left, key, value)
        elif key > root.key:
            root.right = self._delete_b(root.right, key, value)
        elif key == root.key:
            if value.bin_id < root.value.bin_id:
                root.left = self._delete_b(root.left, key, value)
            elif value.bin_id > root.value.bin_id:
                root.right = self._delete_b(root.right, key, value)
            else:
                if not root.left:
                    return root.right
                elif not root.right:
                    return root.left
                temp = self.min_key_node(root.right)
                root.key = temp.key
                root.value = temp.value
                root.right = self._delete_b(root.right, temp.key, temp.value)
        if not root:
            return root

        self.update_height(root)
        balance = self.isbalance(root)

        # Left rotation
        if balance > 1 and self.isbalance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.isbalance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.isbalance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.isbalance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
