class MatrixDescriptor(object):

    def __init__(self, names):
        self._matrices = dict()

        for name in names:
            self._matrices[name] = None

    def get_names(self):
        return self._matrices.keys()

    def set_matrix(self, name, item):
        """
        Set the Matrix with the given name to the given value
        """
        raise NotImplementedError("Should be implemented by derived classes")

    def get_matrix(self, name):
        raise NotImplementedError("Should be implemented by derived classes")

    def update(self, **input):
        """
        Performs any updates of the matrices if needed. Applications should
        provide the actual implementation
        """
        pass

    def __getitem__(self, item):

        if item not in self.get_names():
            raise IndexError("Invalid index: " + item + " not in " + str(self.get_names()))

        return self.get_matrix(name=item)

    def __setitem__(self, key, value):
        self.set_matrix(name=key, item=value)

    def __len__(self):
        return len(self.get_names())


class MatrixDescriptionIterator:
    """
    Helper class to assist iteration over the matrices in
    a MatrixDescriptor
    """

    def __init__(self, matrix_descriptor):

        if isinstance(matrix_descriptor, MatrixDescriptor) == False:
            raise ValueError("Only MatrixDescription and its subclasses should be used")

        self._matrix_descriptor = matrix_descriptor
        self._name_counter = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self._name_counter >= len(self._matrix_descriptor):
            raise StopIteration

        current_name = self._matrix_descriptor.get_names()[self._name_counter]
        current_map = self._matrix_descriptor[current_name]
        self._name_counter += 1

        return current_name, current_map