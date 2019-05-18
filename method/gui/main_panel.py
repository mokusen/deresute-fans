import wx
import datetime
from method.models import connect_mysql, handle_yaml


class MainGui(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300, 330))
        panel = MainPanel(self)
        self.Center()
        self.Show()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.input_number = 5
        self.defalut_size = (120, 30)
        self.defalut_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Meiryo UI')
        self.idol_list = connect_mysql.select_idot_base()
        self.__myinit()

    def __myinit(self):
        idol_panel = self.__idot_panel()
        fans_panel = self.__fans_panel()
        time_panel = self.__time_panel()
        regi_panel = self.__regi_panel()
        restore_panel = self.__restore_panel()

        base_layout = wx.GridBagSizer(0, 0)
        base_layout.Add(idol_panel, (0, 0), (1, 1), flag=wx.EXPAND | wx.LEFT, border=20)
        base_layout.Add(fans_panel, (0, 1), (1, 1), flag=wx.EXPAND)
        base_layout.Add(time_panel, (1, 0), (1, 2), flag=wx.EXPAND | wx.LEFT, border=20)
        base_layout.Add(regi_panel, (2, 0), (1, 2), flag=wx.EXPAND | wx.LEFT, border=20)
        base_layout.Add(restore_panel, (3, 0), (1, 2), flag=wx.EXPAND | wx.LEFT, border=20)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(base_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(layout)

    def __idot_panel(self):
        idol_name = wx.StaticText(self, wx.ID_ANY, 'アイドル名', size=self.defalut_size, style=wx.TE_CENTER)
        self.idol_input_list = [wx.ComboBox(self, wx.ID_ANY, '', choices=self.idol_list, style=wx.CB_DROPDOWN) for _ in range(self.input_number)]

        # フォントサイズ設定
        idol_name.SetFont(self.defalut_font)
        for idol_input in self.idol_input_list:
            idol_input.SetFont(self.defalut_font)

        # レイアウト調整
        base_layout = wx.GridBagSizer(0, 0)
        base_layout.Add(idol_name, (0, 0), (1, 1), flag=wx.EXPAND)
        for idol_index in range(self.input_number):
            base_layout.Add(self.idol_input_list[idol_index], (idol_index + 1, 0), (1, 1), flag=wx.EXPAND)
        return base_layout

    def __fans_panel(self):
        fans = wx.StaticText(self, wx.ID_ANY, 'ファン人数', size=self.defalut_size, style=wx.TE_CENTER)
        self.fans_input_list = [wx.TextCtrl(self, wx.ID_ANY, '') for _ in range(self.input_number)]

        # フォントサイズ設定
        fans.SetFont(self.defalut_font)
        for fans_input in self.fans_input_list:
            fans_input.SetFont(self.defalut_font)

        # レイアウト調整
        base_layout = wx.GridBagSizer(0, 0)
        base_layout.Add(fans, (0, 0), (1, 1), flag=wx.EXPAND)
        for fan_index in range(self.input_number):
            base_layout.Add(self.fans_input_list[fan_index], (fan_index + 1, 0), (1, 1), flag=wx.EXPAND)
        return base_layout

    def __time_panel(self):
        time_text = wx.StaticText(self, wx.ID_ANY, '登録時間', size=self.defalut_size, style=wx.TE_CENTER)
        self.time_input = wx.TextCtrl(self, wx.ID_ANY, '', size=self.defalut_size)

        # フォントサイズ設定
        time_text.SetFont(self.defalut_font)
        self.time_input.SetFont(self.defalut_font)

        # レイアウト調整
        base_layout = wx.GridBagSizer(0, 0)
        base_layout.Add(time_text, (0, 0), (1, 1), flag=wx.EXPAND)
        base_layout.Add(self.time_input, (0, 1), (1, 1), flag=wx.EXPAND)
        return base_layout

    def __regi_panel(self):
        register_button = wx.Button(self, wx.ID_ANY, '登　録')

        # フォントサイズ設定
        register_button.SetFont(self.defalut_font)

        # 登録機能付与
        register_button.Bind(wx.EVT_BUTTON, self.regi_date)
        return register_button

    def __restore_panel(self):
        restore_button = wx.Button(self, wx.ID_ANY, '前回入力を復元する')

        # フォントサイズ設定
        restore_button.SetFont(self.defalut_font)

        # 登録機能付与
        restore_button.Bind(wx.EVT_BUTTON, self.restore_date)
        return restore_button

    def regi_date(self, event):
        message, idol_list, fans_list = self._MainPanel__check_input_date()
        if message != '':
            return wx.MessageBox(message, "入力エラー", wx.ICON_ERROR)
        create_ts = self.time_input.GetValue()
        dlg = wx.MessageDialog(None, "登録を開始して良いですか？", ' 登録内容確認', wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            if create_ts != '':
                for index in range(len(idol_list)):
                    connect_mysql.insert_idol_fans(idol_list[index], fans_list[index], create_ts)
            else:
                for index in range(len(idol_list)):
                    connect_mysql.insert_idol_fans(idol_list[index], fans_list[index], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            wx.MessageBox("登録完了しました。", "登録完了", wx.ICON_INFORMATION)

            # 登録情報を一時保存する
            before_date_yaml = {'idol_list': {index: idol_id for index, idol_id in enumerate(idol_list)},
                                'fans_list': {index: fans for index, fans in enumerate(fans_list)}}
            handle_yaml.outputBeforeDate(before_date_yaml)
        dlg.Destroy()

    def __check_input_date(self):
        return_message = ''
        idol_list = [idol_input.GetSelection()+1 for idol_input in self.idol_input_list if idol_input.GetSelection() != -1]
        fans_list = [fans_input.GetValue() for fans_input in self.fans_input_list if fans_input.GetValue() != '']

        # 入力されていない場合は、エラーとする
        if len(fans_list) == 0 and len(idol_list) == 0:
            return_message += "登録するアイドルとファン人数を入力してください。\n"

        # 入力アイドルとファン人数項目数が一致するか
        if len(fans_list) != len(idol_list):
            return_message += "アイドルとファン人数は対になるように入力してください\n"

        # 整数チェック
        try:
            fans_list = [int(fans_input) for fans_input in fans_list]
        except:
            return_message += "ファン人数は整数で入力してください。\n"
        return return_message[:-1], idol_list, fans_list

    def restore_date(self, event):
        before_date = handle_yaml.getBeforeDate()

        # 前回の情報を入力欄に復元する
        for index in range(len(before_date["idol_list"])):
            self.idol_input_list[index].SetSelection(before_date["idol_list"][index]-1)
            self.fans_input_list[index].SetValue(str(before_date["fans_list"][index]))


def callMainGui():
    app = wx.App(False)
    MainGui(None, wx.ID_ANY, title=u'アイドルファンカウンター')
    app.MainLoop()
