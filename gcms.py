from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.bins = AVLTree()
        self.objects = AVLTree()
        self.bin_id = AVLTree()

    def add_bin(self, bin_id, capacity):
        new_bin = Bin(bin_id, capacity)
        self.bins.insert_bin(capacity, new_bin)
        self.bin_id.insert_object(bin_id, new_bin)


    def add_object(self, object_id, size, color):
        object = Object(object_id, size, color)
        try:
            node = self.bins.search_bin(size, color)
            if not node:
                raise NoBinFoundException()
            bin_instance = node.value
            bin_instance.add_object(object)
            self.objects.insert_object(object_id, (size, node.value))
            original_cap = bin_instance.capacity
            new_cap = bin_instance.capacity - size
            bin_instance.capacity = new_cap
            self.bins.delete_bin(original_cap, bin_instance)
            self.bins.insert_bin(new_cap, bin_instance)
        except:
            raise NoBinFoundException()

    def delete_object(self, object_id):
        try:
            # Implement logic to remove an object from its bin
            node = self.objects.search_object_bin_id(object_id)
            bin_instance = node.value[1]
            bin_instance.remove_object(object_id)
            original_cap = bin_instance.capacity
            new_cap = bin_instance.capacity + node.value[0]
            self.bins.delete_bin(original_cap, bin_instance)
            bin_instance.capacity = new_cap
            self.bins.insert_bin(new_cap, bin_instance)
            self.objects.delete_object(object_id)
        except:
            pass


    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        bin_inst = self.bin_id.search_object_bin_id(bin_id).value
        lst = self.objects_list(bin_inst)
        ans = (bin_inst.capacity,lst)
        return ans

    def object_info(self, object_id):
        try:
            # returns the bin_id in which the object is stored
            node = self.objects.search_object_bin_id(object_id)
            return node.value[1].bin_id
        except:
            pass

    def objects_list(self, bin_inst):
        lst = []
        root = bin_inst.object_ids_in_bin.root
        self._inorder(root, lst)
        return lst

    def _inorder(self, root, lst):
        if root:
            self._inorder(root.left, lst)
            lst.append(root.key)
            self._inorder(root.right, lst)
