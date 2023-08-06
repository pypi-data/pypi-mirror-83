import copy

from PyQt5 import QtCore


class AvailableGenesModel(QtCore.QAbstractListModel):

    def __init__(self, *args, **kwargs):

        super(AvailableGenesModel, self).__init__(*args, **kwargs)

        self._genes = []

        self._genes_default = []

    def clear(self):

        self._genes = []

        self._genes_default()

        self.layoutChanged.emit()

    def data(self, index, role):
        """Get the data at a given index for a given role.

        Args:
            index (QtCore.QModelIndex): the index
            role (int): the role

        Returns:
            QtCore.QVariant: the data
        """

        if not index.isValid():
            return QtCore.QVariant()

        if not self._genes:
            return QtCore.QVariant()

        idx = index.row()

        if role == QtCore.Qt.DisplayRole:
            return self._genes[idx]

    def flags(self, index):
        """Return the flags of an itme with a given index.

        Args:
            index (PyQt5.QtCore.QModelIndex): the index

        Returns:
            int: the flag
        """

        if index.isValid():
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled

    def remove_items(self, items):
        """
        """

        indexes = []

        for item in items:
            try:
                indexes.append(self._genes.index(item))
            except ValueError:
                continue

        indexes.reverse()

        for idx in indexes:
            self.beginRemoveRows(QtCore.QModelIndex(), idx, idx)
            del self._genes[idx]
            self.endRemoveRows()

    def rowCount(self, parent=None):
        """Returns the number of genes.
        """

        return len(self._genes)

    @property
    def genes(self):

        return self._genes

    @genes.setter
    def genes(self, genes):

        self._genes = genes

        self._genes_default = copy.copy(genes)

        self.layoutChanged.emit()

    def reset(self):

        self._genes = copy.copy(self._genes_default)

        self.layoutChanged.emit()
