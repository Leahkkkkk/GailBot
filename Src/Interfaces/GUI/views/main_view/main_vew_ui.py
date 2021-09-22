# Local imports
from .main_ui_variables import *
# Third party imports
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        # Setup central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        # Setup Main Widget
        self.mainWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainWidget.setGeometry(QtCore.QRect(9, 10, 781, 541))
        self.mainWidget.setObjectName("mainWidget")
        # Setup Main Layout
        self.mainVerticalLayout = QtWidgets.QVBoxLayout()
        self.mainVerticalLayout.setContentsMargins(0,0,0,0)
        self.mainVerticalLayout.setObjectName("mainVerticalLayout")
        self.mainVerticalLayout.addWidget(self.mainWidget)
        #### Add objects to the main layout ####
        self.setupMainUi(self.mainWidget,self.mainVerticalLayout)
        ####
        # Setup Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        #### Add menus to menubar ####
        self.setupMenuBarUi(self.menubar)
        ####
        MainWindow.setMenuBar(self.menubar)
        # Setup Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        #### Add widgets to status bar ####
        self.setupStatusBarUi(self.statusbar)
        ####
        MainWindow.setStatusBar(self.statusbar)
        # Set MainWindow attributes
        MainWindow.setWindowTitle(MAIN_WINDOW_TITLE)

    def setupMainUi(self, parentWidget : QtWidgets.QWidget,
            parentLayout : QtWidgets.QLayout)  -> None:
        self.setupMainUiFirstRow(parentWidget, parentLayout)

    def setupMainUiFirstRow(self, parentWidget : QtWidgets.QWidget,
            parentLayout : QtWidgets.QLayout)  -> None:
        containerWidget = QtWidgets.QWidget(parentWidget)
        # Adding layouts
        containerLayout = QtWidgets.QHBoxLayout(containerWidget)
        containerWidget.setLayout(containerLayout)
        optionsLayout = QtWidgets.QVBoxLayout()
        # Adding to options layout
        optionsLayout.addWidget(
            QtWidgets.QLabel(FIRST_ROW_TEXT_LABEL_TEXT,containerWidget))
        optionsLayout.addWidget(
            QtWidgets.QLabel(
                FIRST_ROW_DESCRIPTION_LABEL,containerWidget))
        pushBtn = QtWidgets.QPushButton(
            FIRST_ROW_BUTTON_TEXT,containerWidget)
        pushBtn.setObjectName("staertButton")
        optionsLayout.addWidget(pushBtn)
        # Adding to container layout
        containerLayout.addWidget(QtWidgets.QLabel("ICON",containerWidget))
        containerLayout.addLayout(optionsLayout)
        parentLayout.addWidget(containerWidget)


    def setupMenuBarUi(self, menubar : QtWidgets.QMenuBar) -> None:
        pass

    def setupStatusBarUi(self, statusbar : QtWidgets.QStatusBar) -> None:
        pass




