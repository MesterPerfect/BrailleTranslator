import wx

class BrailleTranslator(wx.Frame):
    def __init__(self, parent, title):
        super(BrailleTranslator, self).__init__(parent, title=title, size=(800, 600))
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        header_label = wx.StaticText(panel, label="Braille Translator", style=wx.ALIGN_CENTER)
        header_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header_label.SetFont(header_font)

        vbox.Add(header_label, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        type_conversion_box = wx.StaticBox(panel, label="Conversion Type")
        type_conversion_box_sizer = wx.StaticBoxSizer(type_conversion_box, wx.VERTICAL)

        self.en2br_radio = wx.RadioButton(panel, label="English to Braille", style=wx.RB_GROUP)
        self.br2en_radio = wx.RadioButton(panel, label="Braille to English")

        type_conversion_box_sizer.Add(self.en2br_radio, flag=wx.ALL, border=10)
        type_conversion_box_sizer.Add(self.br2en_radio, flag=wx.ALL, border=10)

        vbox.Add(type_conversion_box_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        in_text_label = wx.StaticText(panel, label="Input Text:")
        in_text_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        in_text_label.SetFont(in_text_font)

        self.in_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 150))

        out_text_label = wx.StaticText(panel, label="Output Text:")
        out_text_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        out_text_label.SetFont(out_text_font)

        self.out_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(300, 150))

        vbox.Add(in_text_label, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        vbox.Add(self.in_text_ctrl, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(out_text_label, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        vbox.Add(self.out_text_ctrl, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        convert_btn = wx.Button(panel, label="Convert")
        convert_btn.Bind(wx.EVT_BUTTON, self.on_convert)

        vbox.Add(convert_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        footer_label = wx.StaticText(panel, label="Programmed by Your Name")
        footer_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        footer_label.SetFont(footer_font)

        vbox.Add(footer_label, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(vbox)

        self.en2br_radio.SetValue(True)
        self.on_conversion_type_changed()

        self.Bind(wx.EVT_RADIOBUTTON, self.on_conversion_type_changed, id=self.en2br_radio.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.on_conversion_type_changed, id=self.br2en_radio.GetId())

    def on_conversion_type_changed(self, event=None):
        conversion_type = "en2br" if self.en2br_radio.GetValue() else "br2en"
        self.in_text_ctrl.SetEditable(conversion_type == "en2br")
        self.out_text_ctrl.SetEditable(conversion_type == "br2en")

    def on_convert(self, event):
        conversion_type = "en2br" if self.en2br_radio.GetValue() else "br2en"
        input_text = self.in_text_ctrl.GetValue()
        if conversion_type == "en2br":
            output_text = self.en2braille(input_text)
        else:
            output_text = self.braille2en(input_text)
        self.out_text_ctrl.SetValue(output_text)

    def en2braille(self, text):
        # English alphabet to Braille Unicode mapping
        english_braille = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛',
            'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝',
            'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥',
            'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
            '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
            '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
            '.': '⠲', ',': '⠂', ':': '⠒', ';': '⠆', '?': '⠦', '!': '⠖',
        }

        braille_text = []
        for char in text.lower():
            braille_char = english_braille.get(char, char)
            braille_text.append(braille_char)

        return ''.join(braille_text)

    def braille2en(self, text):
        # Braille Unicode to English alphabet mapping
        braille_english = {v: k for k, v in self.english_braille.items()}

        english_text = []
        for char in text:
            english_char = braille_english.get(char, char)
            english_text.append(english_char)

        return ''.join(english_text)


if __name__ == '__main__':
    app = wx.App(False)
    frame = BrailleTranslator(None, title="Braille Translator")
    frame.Show()
    app.MainLoop()
