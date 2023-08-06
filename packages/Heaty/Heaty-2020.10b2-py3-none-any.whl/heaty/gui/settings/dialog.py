from functools import partial

from PyQt5 import QtWidgets as qtw
from heaty.gui.settings import settings
from heaty.gui.user_input.form import ButtonBox


class DirTab(qtw.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        settings.Paths.read_config_file()

        main_layout = qtw.QVBoxLayout(self)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        self.setAutoFillBackground(True)

        ico_dir = self.style().standardIcon(qtw.QStyle.SP_DirIcon)

        lbl_proj_dir = qtw.QLabel('<b>Project directory</b>')
        main_layout.addWidget(lbl_proj_dir)
        sub_layout1 = qtw.QHBoxLayout(self)
        main_layout.addLayout(sub_layout1)
        self.led_proj_dir = qtw.QLineEdit(settings.Paths.paths["PROJECT_PATH"], parent)
        sub_layout1.addWidget(self.led_proj_dir)
        btn_proj_dir = qtw.QToolButton(self)
        btn_proj_dir.setIcon(ico_dir)
        btn_proj_dir.clicked.connect(self._select_proj)
        sub_layout1.addWidget(btn_proj_dir)

        lbl_exp_dir = qtw.QLabel('<b>Export directory</b>')
        main_layout.addWidget(lbl_exp_dir)
        sub_layout2 = qtw.QHBoxLayout(self)
        main_layout.addLayout(sub_layout2)
        self.led_exp_dir = qtw.QLineEdit(settings.Paths.paths["EXPORT_PATH"], parent)
        sub_layout2.addWidget(self.led_exp_dir)
        btn_exp_dir = qtw.QToolButton(self)
        btn_exp_dir.setIcon(ico_dir)
        btn_exp_dir.clicked.connect(self._select_exp)
        sub_layout2.addWidget(btn_exp_dir)

        main_layout.addStretch()

    def _select_proj(self):
        folder = qtw.QFileDialog.getExistingDirectory(
            self,
            'Choose project directory...',
            settings.ROOT_PATH,
            qtw.QFileDialog.ShowDirsOnly |
            qtw.QFileDialog.DontUseNativeDialog |
            qtw.QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.led_proj_dir.setText(folder)
            settings.Paths.paths['PROJECT_PATH'] = folder

    def _select_exp(self):
        folder = qtw.QFileDialog.getExistingDirectory(
            self,
            'Choose export directory...',
            settings.ROOT_PATH,
            qtw.QFileDialog.ShowDirsOnly |
            qtw.QFileDialog.DontUseNativeDialog |
            qtw.QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.led_exp_dir.setText(folder)
            settings.Paths.paths['EXPORT_PATH'] = folder

    def set_paths(self) -> bool:
        path_proj = self.led_proj_dir.text()
        path_exp = self.led_exp_dir.text()
        if settings.Paths.validate(path_proj):
            settings.Paths.paths['PROJECT_PATH'] = path_proj
        else:
            qtw.QMessageBox.critical(
                self,
                'Input Error',
                f'Path "{path_proj}" does not exist'
            )
            return False
        if settings.Paths.validate(path_exp):
            settings.Paths.paths['EXPORT_PATH'] = path_exp
        else:
            qtw.QMessageBox.critical(
                self,
                'Input Error',
                f'Path "{path_exp}" does not exist'
            )
            return False
        return True


class UnitsTab(qtw.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        units = settings.Units.units
        self.wid_units = {label: qtw.QLineEdit(unit, self) for label, unit in units.items()}
        form_layout = qtw.QFormLayout()
        for lbl, led in self.wid_units.items():
            form_layout.addRow(qtw.QLabel(lbl), led)
            led.editingFinished.connect(partial(self._validate_unit, lbl))
        main_layout.addLayout(form_layout)

    def _validate_unit(self, label: str):
        unit = self.wid_units[label].text()
        if not settings.Units.validate(label, unit):
            qtw.QMessageBox.critical(
                self,
                'Input Error',
                f'Invalid unit "{unit}" for quantity "{label}"'
            )
            self.wid_units[label].setFocus()

    def set_units(self) -> bool:
        for label in self.wid_units.keys():
            unit = self.wid_units[label].text()
            if not settings.Units.validate(label, unit):
                qtw.QMessageBox.critical(
                    self,
                    'Input Error',
                    f'Invalid unit "{unit}" for quantity "{label}"'
                )
                self.wid_units[label].setFocus()
                return False
            else:
                settings.Units.units[label] = unit
        return True


# noinspection PyArgumentList
class SettingsDialog(qtw.QDialog):

    def __init__(self, parent):
        super().__init__(parent, modal=True)
        self.setWindowTitle('Preferences')
        self.resize(400, 400)

        self.controller = parent.controller

        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        self.tab = qtw.QTabWidget(self)
        self.tab.setUsesScrollButtons(False)
        self.tab.addTab(DirTab(self.tab), 'Default Paths')
        self.tab.addTab(UnitsTab(self.tab), 'Default Units')
        main_layout.addWidget(self.tab)

        buttonbox = ButtonBox(self, labels=['Submit', 'Discard'], slots=[self.pre_accept, self.reject])
        buttonbox.buttons['Discard'].setDefault(True)
        main_layout.addWidget(buttonbox)

        self.show()

    def pre_accept(self):
        current_tab = self.tab.currentWidget()
        if isinstance(current_tab, DirTab):
            if current_tab.set_paths():  # put the paths entered by the user into paths settings
                settings.Paths.write_config_file()
                self.accept()
        if isinstance(current_tab, UnitsTab):
            if current_tab.set_units():  # put the units entered by the user into units settings
                settings.Units.write_config_file()
                self.controller.update_tree()
                self.accept()
