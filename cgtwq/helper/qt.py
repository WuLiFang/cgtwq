# -*- coding=UTF-8 -*-
"""Helper for cgtwq with qt.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

import cgtwq
from Qt.QtWidgets import (QApplication, QDialog, QLabel,  # type: ignore
                          QLineEdit, QMessageBox, QPushButton, QVBoxLayout)
from six import text_type


def application():
    """Get QApplication instance, create one if needed.  """

    app = QApplication.instance()

    if not app:
        app = QApplication(sys.argv)
    return app


def ask_login(parent=None):
    """Ask login with a dialog.
        parent (QWidget, optional): Defaults to None. Parent widget.

    Returns:
        cgtwq.AccountInfo: Account logged in.
    """

    _app = application()
    dialog = QDialog(parent)
    account_input = QLineEdit()
    password_input = QLineEdit()
    _setup_login_dialog(dialog, account_input, password_input)

    while True:
        dialog.exec_()
        if dialog.result() == QDialog.Rejected:
            raise ValueError('Rejected')
        account, password = account_input.text(), password_input.text()
        try:
            return cgtwq.login(account, password)
        except (ValueError, cgtwq.AccountNotFoundError, cgtwq.PasswordError) as ex:
            msg = text_type(ex)
            QMessageBox.critical(parent, '登录失败', msg)


def _setup_login_dialog(dialog, account_input, password_input):
    dialog.setWindowTitle('登录CGTeamWork')
    account_input.setPlaceholderText('CGTeamwork账号名')
    password_input.setPlaceholderText('密码')
    password_input.setEchoMode(QLineEdit.Password)

    ok_button = QPushButton('登录')
    ok_button.setDefault(True)
    ok_button.clicked.connect(dialog.accept)

    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel('帐号'))
    layout.addWidget(account_input)
    layout.addWidget(QLabel('密码'))
    layout.addWidget(password_input)
    layout.addWidget(ok_button)
    dialog.setLayout(layout)
