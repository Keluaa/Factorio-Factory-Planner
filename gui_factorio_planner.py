# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui_factorio_planner.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 530)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Items_List_Label = QtWidgets.QLabel(self.centralwidget)
        self.Items_List_Label.setObjectName("Items_List_Label")
        self.verticalLayout.addWidget(self.Items_List_Label)
        self.Items_Categories = QtWidgets.QComboBox(self.centralwidget)
        self.Items_Categories.setObjectName("Items_Categories")
        self.verticalLayout.addWidget(self.Items_Categories)
        self.Item_Search = QtWidgets.QLineEdit(self.centralwidget)
        self.Item_Search.setStyleSheet("QLineEdit {\n"
"    background: #ffffff;\n"
"    background-image: url(img/search.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: left;\n"
"    color: #252424;\n"
"    padding: 2 2 2 20;\n"
"}")
        self.Item_Search.setMaxLength(50)
        self.Item_Search.setObjectName("Item_Search")
        self.verticalLayout.addWidget(self.Item_Search)
        self.Items_List = QtWidgets.QListWidget(self.centralwidget)
        self.Items_List.setAlternatingRowColors(True)
        self.Items_List.setObjectName("Items_List")
        self.verticalLayout.addWidget(self.Items_List)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Item_Count = QtWidgets.QLineEdit(self.centralwidget)
        self.Item_Count.setMinimumSize(QtCore.QSize(0, 25))
        self.Item_Count.setMaxLength(20)
        self.Item_Count.setClearButtonEnabled(False)
        self.Item_Count.setObjectName("Item_Count")
        self.horizontalLayout.addWidget(self.Item_Count)
        self.Item_Add = QtWidgets.QPushButton(self.centralwidget)
        self.Item_Add.setMinimumSize(QtCore.QSize(0, 30))
        self.Item_Add.setObjectName("Item_Add")
        self.horizontalLayout.addWidget(self.Item_Add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Needs_List_Label = QtWidgets.QLabel(self.centralwidget)
        self.Needs_List_Label.setObjectName("Needs_List_Label")
        self.verticalLayout_2.addWidget(self.Needs_List_Label)
        self.Needs_List = QtWidgets.QTableWidget(self.centralwidget)
        self.Needs_List.setColumnCount(2)
        self.Needs_List.setObjectName("Needs_List")
        self.Needs_List.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Needs_List.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Needs_List.setHorizontalHeaderItem(1, item)
        self.Needs_List.horizontalHeader().setVisible(True)
        self.Needs_List.horizontalHeader().setCascadingSectionResizes(False)
        self.Needs_List.horizontalHeader().setDefaultSectionSize(50)
        self.Needs_List.horizontalHeader().setHighlightSections(True)
        self.Needs_List.horizontalHeader().setMinimumSectionSize(50)
        self.Needs_List.horizontalHeader().setSortIndicatorShown(True)
        self.Needs_List.horizontalHeader().setStretchLastSection(True)
        self.Needs_List.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.Needs_List)
        self.Need_Remove = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Need_Remove.sizePolicy().hasHeightForWidth())
        self.Need_Remove.setSizePolicy(sizePolicy)
        self.Need_Remove.setMinimumSize(QtCore.QSize(0, 30))
        self.Need_Remove.setObjectName("Need_Remove")
        self.verticalLayout_2.addWidget(self.Need_Remove, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Results_Label = QtWidgets.QLabel(self.centralwidget)
        self.Results_Label.setObjectName("Results_Label")
        self.verticalLayout_3.addWidget(self.Results_Label)
        self.Results = QtWidgets.QTreeWidget(self.centralwidget)
        self.Results.setStyleSheet("QTreeView::branch:has-siblings:!adjoins-item {\n"
"    border-image: url(img/vline.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"    border-image: url(img/branch-more.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(img/branch-end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"        border-image: none;\n"
"        image: url(img/branch-closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"        border-image: none;\n"
"        image: url(img/branch-open.png);\n"
"}")
        self.Results.setAnimated(True)
        self.Results.setObjectName("Results")
        self.Results.headerItem().setText(0, "1")
        self.Results.header().setVisible(False)
        self.Results.header().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.Results)
        self.Compute_Button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Compute_Button.sizePolicy().hasHeightForWidth())
        self.Compute_Button.setSizePolicy(sizePolicy)
        self.Compute_Button.setMinimumSize(QtCore.QSize(0, 30))
        self.Compute_Button.setObjectName("Compute_Button")
        self.verticalLayout_3.addWidget(self.Compute_Button, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.Items_List_Label.setBuddy(self.Items_List)
        self.Needs_List_Label.setBuddy(self.Needs_List)
        self.Results_Label.setBuddy(self.Results)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Items_Categories, self.Items_List)
        MainWindow.setTabOrder(self.Items_List, self.Item_Count)
        MainWindow.setTabOrder(self.Item_Count, self.Item_Add)
        MainWindow.setTabOrder(self.Item_Add, self.Needs_List)
        MainWindow.setTabOrder(self.Needs_List, self.Need_Remove)
        MainWindow.setTabOrder(self.Need_Remove, self.Results)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Factory Planner"))
        self.Items_List_Label.setText(_translate("MainWindow", "Items"))
        self.Item_Add.setText(_translate("MainWindow", "Add Item"))
        self.Needs_List_Label.setText(_translate("MainWindow", "Needs"))
        self.Needs_List.setSortingEnabled(True)
        item = self.Needs_List.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Count"))
        item = self.Needs_List.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item"))
        self.Need_Remove.setText(_translate("MainWindow", "Remove Item"))
        self.Results_Label.setText(_translate("MainWindow", "Factory"))
        self.Compute_Button.setText(_translate("MainWindow", "Compute Factory"))


