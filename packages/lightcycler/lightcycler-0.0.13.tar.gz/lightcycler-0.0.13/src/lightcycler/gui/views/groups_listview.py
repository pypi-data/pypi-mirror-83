from PyQt5 import QtCore, QtGui, QtWidgets


class GroupsListView(QtWidgets.QListView):
    """This class implements an interface for listviews onto which data can be dropped in.
    """

    def keyPressEvent(self, event):
        """Event handler for keyboard interaction.

        Args:
            event (PyQt5.QtGui.QKeyEvent): the keyboard event
        """

        key = event.key()

        if key == QtCore.Qt.Key_Delete:

            groups_model = self.model()
            if groups_model is None:
                return

            selected_groups = [groups_model.data(index, QtCore.Qt.DisplayRole) for index in self.selectedIndexes()]

            groups_model.remove_groups(selected_groups)
            if groups_model.rowCount() > 0:
                index = groups_model.index(groups_model.rowCount()-1)
                self.setCurrentIndex(index)

        elif key == QtCore.Qt.Key_Space:

            groups_model = self.model()
            if groups_model is None:
                return

            selected_indexes = self.selectedIndexes()
            if not selected_indexes:
                return

            selected_row = selected_indexes[0].row()

            groups_model.group_control = selected_row

        else:
            super(GroupsListView, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        """Event handler for mouse interaction.

        Args:
            event (PyQt5.QtGui.QMouseEvent): the mouse event
        """

        super(GroupsListView, self).mousePressEvent(event)

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                groups_model = self.model()
                if groups_model is None:
                    return
                groups_model.on_display_group_contents(self.currentIndex())
                return
