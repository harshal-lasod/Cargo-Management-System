from avl import *
from node import *
from object import *

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.object_ids_in_bin = AVLTree()

    def add_object(self, object):
        # Implement logic to add an object to this bin
        self.object_ids_in_bin.insert_object(object.object_id, object.size)

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        self.object_ids_in_bin.delete_object(object_id)

