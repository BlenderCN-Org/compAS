# -*- coding: utf-8 -*-

import System

from System.Windows.Forms import Button
from System.Windows.Forms import DialogResult
from System.Windows.Forms import DataGridViewColumnSortMode
from System.Windows.Forms import FlowLayoutPanel
from System.Windows.Forms import TableLayoutPanel
from System.Windows.Forms import AnchorStyles
from System.Windows.Forms import FlowDirection
from System.Windows.Forms import BorderStyle
from System.Windows.Forms import DockStyle
from System.Windows.Forms import RowStyle
from System.Windows.Forms import SizeType

from _form import Form
from _form import make_table


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Mar 17, 2015'


class TableForm(Form):
    """"""

    def __init__(self, headers, rows, title=None, width=None, height=None):
        self.headers = headers
        self.rows = rows
        super(TableForm, self).__init__(title, width, height)

    def init(self):
        table = make_table('make_blocks')
        self.table = table
        table.ColumnCount = len(self.headers)
        for i, header in enumerate(self.headers):
            table.Columns[i].Name = header
            table.Columns[i].SortMode = DataGridViewColumnSortMode.NotSortable
        for i, row in enumerate(self.rows):
            table.Rows.Add(*row)
            # table.Rows.Add(*row[1:])
            # table.Rows[table.RowCount - 1].HeaderCell.Value = str(row[0])
        ok = Button()
        ok.Text = 'OK'
        ok.DialogResult = DialogResult.OK
        cancel = Button()
        cancel.Text = 'Cancel'
        cancel.DialogResult = DialogResult.Cancel
        buttonlayout = FlowLayoutPanel()
        buttonlayout.Height = 30
        buttonlayout.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        buttonlayout.FlowDirection = FlowDirection.RightToLeft
        buttonlayout.BorderStyle = BorderStyle.None
        buttonlayout.Controls.Add(cancel)
        buttonlayout.Controls.Add(ok)
        formlayout = TableLayoutPanel()
        formlayout.Dock = DockStyle.Fill
        formlayout.BorderStyle = BorderStyle.None
        formlayout.ColumnCount = 1
        formlayout.RowCount = 2
        formlayout.RowStyles.Add(RowStyle(SizeType.Percent, 100))
        formlayout.Controls.Add(table, 0, 0)
        formlayout.Controls.Add(buttonlayout, 0, 1)
        self.Controls.Add(formlayout)

    def on_form_closed(self, sender, e):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    headers = ['A', 'B', 'C', 'D']
    rows = [[i, i, i, i] for i in range(100)]

    # headers = [
    #     {'data' : 'A', 'attr' : {'sortable' : True, 'readonly': True, 'bgcolor' : (), 'color' : ()}},
    #     {'data' : 'B', 'attr' : {}},
    # ]

    form = TableForm(headers, rows)
    form.show()
