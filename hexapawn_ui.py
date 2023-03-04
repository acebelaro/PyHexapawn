# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hexapawn_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widgetHexapawn(object):
    def setupUi(self, widgetHexapawn):
        widgetHexapawn.setObjectName("widgetHexapawn")
        widgetHexapawn.resize(1053, 421)
        self.grpBoard = QtWidgets.QGroupBox(widgetHexapawn)
        self.grpBoard.setGeometry(QtCore.QRect(20, 10, 341, 341))
        self.grpBoard.setObjectName("grpBoard")
        self.btnPawn0 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn0.setGeometry(QtCore.QRect(20, 20, 101, 101))
        self.btnPawn0.setText("")
        self.btnPawn0.setObjectName("btnPawn0")
        self.btnPawn1 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn1.setGeometry(QtCore.QRect(120, 20, 101, 101))
        self.btnPawn1.setText("")
        self.btnPawn1.setObjectName("btnPawn1")
        self.btnPawn3 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn3.setGeometry(QtCore.QRect(20, 120, 101, 101))
        self.btnPawn3.setText("")
        self.btnPawn3.setObjectName("btnPawn3")
        self.btnPawn4 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn4.setGeometry(QtCore.QRect(120, 120, 101, 101))
        self.btnPawn4.setText("")
        self.btnPawn4.setObjectName("btnPawn4")
        self.btnPawn5 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn5.setGeometry(QtCore.QRect(220, 120, 101, 101))
        self.btnPawn5.setText("")
        self.btnPawn5.setObjectName("btnPawn5")
        self.btnPawn2 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn2.setGeometry(QtCore.QRect(220, 20, 101, 101))
        self.btnPawn2.setText("")
        self.btnPawn2.setObjectName("btnPawn2")
        self.btnPawn7 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn7.setGeometry(QtCore.QRect(120, 220, 101, 101))
        self.btnPawn7.setText("")
        self.btnPawn7.setObjectName("btnPawn7")
        self.btnPawn6 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn6.setGeometry(QtCore.QRect(20, 220, 101, 101))
        self.btnPawn6.setText("")
        self.btnPawn6.setObjectName("btnPawn6")
        self.btnPawn8 = QtWidgets.QPushButton(self.grpBoard)
        self.btnPawn8.setGeometry(QtCore.QRect(220, 220, 101, 101))
        self.btnPawn8.setText("")
        self.btnPawn8.setObjectName("btnPawn8")
        self.grpInfo = QtWidgets.QGroupBox(widgetHexapawn)
        self.grpInfo.setGeometry(QtCore.QRect(20, 360, 341, 51))
        self.grpInfo.setTitle("")
        self.grpInfo.setObjectName("grpInfo")
        self.lblPlayerToMove = QtWidgets.QLabel(self.grpInfo)
        self.lblPlayerToMove.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.lblPlayerToMove.setObjectName("lblPlayerToMove")
        self.btnPlayerToMove = QtWidgets.QPushButton(self.grpInfo)
        self.btnPlayerToMove.setEnabled(True)
        self.btnPlayerToMove.setGeometry(QtCore.QRect(110, 10, 121, 23))
        self.btnPlayerToMove.setText("")
        self.btnPlayerToMove.setObjectName("btnPlayerToMove")
        self.btnReset = QtWidgets.QPushButton(self.grpInfo)
        self.btnReset.setGeometry(QtCore.QRect(240, 10, 75, 23))
        self.btnReset.setObjectName("btnReset")
        self.grpComputer = QtWidgets.QGroupBox(widgetHexapawn)
        self.grpComputer.setGeometry(QtCore.QRect(370, 10, 671, 401))
        self.grpComputer.setObjectName("grpComputer")
        self.btnComputerMove = QtWidgets.QPushButton(self.grpComputer)
        self.btnComputerMove.setGeometry(QtCore.QRect(10, 20, 211, 191))
        self.btnComputerMove.setText("")
        self.btnComputerMove.setObjectName("btnComputerMove")
        self.grpMoves = QtWidgets.QGroupBox(self.grpComputer)
        self.grpMoves.setGeometry(QtCore.QRect(10, 220, 211, 141))
        self.grpMoves.setTitle("")
        self.grpMoves.setObjectName("grpMoves")
        self.btnMoveRandomSelect = QtWidgets.QPushButton(self.grpComputer)
        self.btnMoveRandomSelect.setGeometry(QtCore.QRect(14, 370, 211, 23))
        self.btnMoveRandomSelect.setObjectName("btnMoveRandomSelect")
        self.btnResetIntelligence = QtWidgets.QPushButton(self.grpComputer)
        self.btnResetIntelligence.setGeometry(QtCore.QRect(500, 20, 161, 23))
        self.btnResetIntelligence.setObjectName("btnResetIntelligence")
        self.tableResults = QtWidgets.QTableWidget(self.grpComputer)
        self.tableResults.setGeometry(QtCore.QRect(230, 50, 431, 341))
        self.tableResults.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableResults.setObjectName("tableResults")
        self.tableResults.setColumnCount(1)
        self.tableResults.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableResults.setHorizontalHeaderItem(0, item)
        self.tableResults.horizontalHeader().setStretchLastSection(True)

        self.retranslateUi(widgetHexapawn)
        QtCore.QMetaObject.connectSlotsByName(widgetHexapawn)

    def retranslateUi(self, widgetHexapawn):
        _translate = QtCore.QCoreApplication.translate
        widgetHexapawn.setWindowTitle(_translate("widgetHexapawn", "Hexapawn"))
        self.grpBoard.setTitle(_translate("widgetHexapawn", "Board"))
        self.lblPlayerToMove.setText(_translate("widgetHexapawn", "Player To Move:"))
        self.btnReset.setText(_translate("widgetHexapawn", "Reset"))
        self.grpComputer.setTitle(_translate("widgetHexapawn", "Computer"))
        self.btnMoveRandomSelect.setText(_translate("widgetHexapawn", "  RANDOM SELECT"))
        self.btnResetIntelligence.setText(_translate("widgetHexapawn", "RESET INTELLIGENCE"))
        item = self.tableResults.horizontalHeaderItem(0)
        item.setText(_translate("widgetHexapawn", "Results"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetHexapawn = QtWidgets.QWidget()
    ui = Ui_widgetHexapawn()
    ui.setupUi(widgetHexapawn)
    widgetHexapawn.show()
    sys.exit(app.exec_())
