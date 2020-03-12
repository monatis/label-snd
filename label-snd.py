import wx
import wx.adv
import glob
import os


class PromptingComboBox(wx.ComboBox) :
    """Inspired by https://stackoverflow.com/questions/50978627/combobox-with-autocomplete-wxpython"""
    
    def __init__(self, parent, on_choice_selected, choices=[], style=0, **par):
        self.on_choice_selected  = on_choice_selected
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, style=style|wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER, choices=choices, **par)
        self.choices = choices
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)
        self.Bind(wx.EVT_KEY_DOWN, self.OnPress)
        self.ignoreEvtText = False
        self.deleteKey = False

    def OnPress(self, event):
        if event.GetKeyCode() == 8:
            self.deleteKey = True
        event.Skip()

    def OnText(self, event):
        currentText = event.GetString()
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return
        if self.deleteKey:
            self.deleteKey = False
            if self.preFound:
                currentText =  currentText[:-1]

        self.preFound = False
        for choice in self.choices :
            if choice.startswith(currentText):
                self.ignoreEvtText = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(currentText))
                self.SetTextSelection(len(currentText), len(choice))
                self.preFound = True
                break

    def on_enter_pressed(self, event):
        txt = self.GetValue()
        self.SetValue("")
        self.on_choice_selected(txt)


class ListPanel(wx.Panel):    
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 350), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.start_playing)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        self.combo_box = PromptingComboBox(self, self.on_save_click, choices=[])
        main_sizer.Add(self.combo_box, 0, wx.ALL | wx.CENTER, 5)
        #save_btn = wx.Button(self, label='Save')
        #save_btn.Bind(wx.EVT_BUTTON, self.on_save_click)
        #main_sizer.Add(save_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(main_sizer)
        self.update_list("input")
        
    
    def start_playing(self, event=None):
        if len(self.files) == 0:
            return False

        index = self.list_ctrl.GetFocusedItem()
        if index == -1:
            index = 0

            self.list_ctrl.Focus(index)

        wx.adv.Sound(self.files[index]).Play(wx.adv.SOUND_ASYNC|wx.adv.SOUND_LOOP)

    def on_save_click(self, txt):
        wx.adv.Sound.Stop()
        index = self.list_ctrl.GetFocusedItem()
        if index >= 0:
            f = open(os.path.join(self.folder, "metadata.csv"), "a+", encoding='utf8')
            f.write(self.files[index].split(os.path.sep)[-1] + "|" + txt + "\n")
            f.close()
            if index + 1 != len(self.files):
                self.list_ctrl.Focus(index + 1)
                self.start_playing()
                
    def update_list(self, folder_path):
        self.folder = folder_path
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, 'No.', width=50)
        self.list_ctrl.InsertColumn(1, 'File Path', width=400)
        self.list_ctrl.InsertColumn(2, 'Status', width=70)
        self.files = glob.glob(folder_path + "/*.wav")
        for i, file in enumerate(self.files):
            self.list_ctrl.InsertItem(i, i+1)
            self.list_ctrl.SetItem(i, 0, str(i+1))
            self.list_ctrl.SetItem(i, 1, file)
            self.list_ctrl.SetItem(i, 2, "-")
            
        self.start_playing()



class MainFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None,
                         title='label-snd - Sound Annotations')
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = ListPanel(self)
        self.create_menu()
        main_sizer.Add(self.panel, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(main_sizer)
        self.Layout()
        main_sizer.Fit(self)
        
    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        select_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Select audio folder...', 'Browse for the folder containing .wav files')
        select_file_menu_item = file_menu.Append(wx.ID_ANY, "Populate choices from...", "Select a .txt file to populate choices in the combo box")
        about_menu_item = file_menu.Append(wx.ID_ABOUT, "About...", "Learn more about this utility")
        menu_bar.Append(file_menu, '&File')
        self.Bind(event=wx.EVT_MENU, handler=self.on_select_folder, source=select_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_select_file, source=select_file_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_about, source=about_menu_item)
        self.SetMenuBar(menu_bar)

    def on_select_folder(self, event):
        title = "Select folder to read sounds from:"
        dlg = wx.DirDialog(self, title, 
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_list(dlg.GetPath())
        dlg.Destroy()

    def on_select_file(self, event):

        with wx.FileDialog(self, "Open text file", wildcard="Text files (*.txt)|*.txt",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf8') as file:
                    choices = [line.rstrip() for line in file.readlines()]
                    self.panel.combo_box.SetItems(choices)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def on_about(self, event):
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("label-snd")
        aboutInfo.SetVersion("0.1")
        aboutInfo.SetDescription("Easily label sound datasets!")
        aboutInfo.SetCopyright("(C) 2020")
        aboutInfo.SetWebSite("https://github.com/monatis/label-snd")
        aboutInfo.AddDeveloper("M. Yusuf Sarıgöz")

        wx.adv.AboutBox(aboutInfo)



if __name__ == '__main__':
    app = wx.App(False)
    main_frame = MainFrame()
    main_frame.Show()
    app.MainLoop()