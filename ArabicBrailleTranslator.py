import wx

class ArabicBrailleTranslator(wx.Frame):
    def __init__(self, parent, title):
        super(ArabicBrailleTranslator, self).__init__(parent, title=title, size=(800, 600))
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        header_label = wx.StaticText(panel, label="برايل | Braille", style=wx.ALIGN_CENTER)
        header_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header_label.SetFont(header_font)

        vbox.Add(header_label, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        type_conversion_box = wx.StaticBox(panel, label="نوع التحويل")
        type_conversion_box_sizer = wx.StaticBoxSizer(type_conversion_box, wx.VERTICAL)

        self.ar2b_radio = wx.RadioButton(panel, label="من الأبجدية إلى برايل", style=wx.RB_GROUP)
        self.b2ar_radio = wx.RadioButton(panel, label="من برايل إلى الأبجدية")

        type_conversion_box_sizer.Add(self.ar2b_radio, flag=wx.ALL, border=10)
        type_conversion_box_sizer.Add(self.b2ar_radio, flag=wx.ALL, border=10)

        vbox.Add(type_conversion_box_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        supported_features_label = wx.StaticText(panel, label="تم دعم:")
        supported_features_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        supported_features_label.SetFont(supported_features_font)

        features_list = wx.StaticText(panel, label="رموز الحروف ( ا - ي )\n"
                                                  "رموز الأعداد و رمز علامة الأعداد (0-9 - علامة الأعداد)\n"
                                                  "رموز التشكيل ( َ - ً - ُ - ٌ - ِ - ٍ - ْ - ّ )\n"
                                                  "رموز علامات التنقيط ( . - ، - : - ؛ - ؟ - ! )")
        features_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        features_list.SetFont(features_font)

        vbox.Add(supported_features_label, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        vbox.Add(features_list, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        in_text_label = wx.StaticText(panel, label="النص العربي:")
        in_text_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        in_text_label.SetFont(in_text_font)

        self.in_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 150))

        out_text_label = wx.StaticText(panel, label="النص برايل:")
        out_text_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        out_text_label.SetFont(out_text_font)

        self.out_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(300, 150))

        vbox.Add(in_text_label, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        vbox.Add(self.in_text_ctrl, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(out_text_label, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        vbox.Add(self.out_text_ctrl, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        convert_btn = wx.Button(panel, label="تحويل")
        convert_btn.Bind(wx.EVT_BUTTON, self.on_convert)

        vbox.Add(convert_btn, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        footer_label = wx.StaticText(panel, label="برمجة سليمان العثمان")
        footer_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        footer_label.SetFont(footer_font)

        vbox.Add(footer_label, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(vbox)

        self.ar2b_radio.SetValue(True)
        self.on_conversion_type_changed()

        self.Bind(wx.EVT_RADIOBUTTON, self.on_conversion_type_changed, id=self.ar2b_radio.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.on_conversion_type_changed, id=self.b2ar_radio.GetId())

    def on_conversion_type_changed(self, event=None):
        conversion_type = "ar2b" if self.ar2b_radio.GetValue() else "b2ar"
        self.in_text_ctrl.SetEditable(conversion_type == "ar2b")
        self.out_text_ctrl.SetEditable(conversion_type == "b2ar")

    def on_convert(self, event):
        conversion_type = "ar2b" if self.ar2b_radio.GetValue() else "b2ar"
        input_text = self.in_text_ctrl.GetValue()
        if conversion_type == "ar2b":
            output_text = self.ar2braille(input_text)
        else:
            output_text = self.braille2ar(input_text)
        self.out_text_ctrl.SetValue(output_text)

    def ar2braille(self, text):
        arabic_letters = {
            'ا': '⠁', 'ب': '⠃', 'ت': '⠞', 'ث': '⠹', 'ج': '⠚', 'ح': '⠓', 'خ': '⠺',
            'د': '⠙', 'ذ': '⠺', 'ر': '⠗', 'ز': '⠵', 'س': '⠎', 'ش': '⠱', 'ص': '⠮',
            'ض': '⠟', 'ط': '⠾', 'ظ': '⠹', 'ع': '⠪', 'غ': '⠳', 'ف': '⠋', 'ق': '⠽',
            'ك': '⠅', 'ل': '⠇', 'م': '⠍', 'ن': '⠝', 'ه': '⠓', 'و': '⠺', 'ي': '⠽',
            '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑', '6': '⠋',
            '7': '⠛', '8': '⠓', '9': '⠊',
            '.': '⠲', ',': '⠂', ':': '⠒', ';': '⠶', '?': '⠦', '!': '⠖',
        }

        braille_text = []
        for char in text:
            braille_char = arabic_letters.get(char, char)
            braille_text.append(braille_char)

        return ''.join(braille_text)

    def braille2ar(self, text):
        arabic_letters = {
            'ا': '⠁', 'ب': '⠃', 'ت': '⠞', 'ث': '⠹', 'ج': '⠚', 'ح': '⠓', 'خ': '⠺',
            'د': '⠙', 'ذ': '⠺', 'ر': '⠗', 'ز': '⠵', 'س': '⠎', 'ش': '⠱', 'ص': '⠮',
            'ض': '⠟', 'ط': '⠾', 'ظ': '⠹', 'ع': '⠪', 'غ': '⠳', 'ف': '⠋', 'ق': '⠽',
            'ك': '⠅', 'ل': '⠇', 'م': '⠍', 'ن': '⠝', 'ه': '⠓', 'و': '⠺', 'ي': '⠽',
            '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑', '6': '⠋',
            '7': '⠛', '8': '⠓', '9': '⠊',
            '.': '⠲', ',': '⠂', ':': '⠒', ';': '⠶', '?': '⠦', '!': '⠖',
        }

        braille_letters = {v: k for k, v in arabic_letters.items()}

        arabic_text = []
        for char in text:
            arabic_char = braille_letters.get(char, char)
            arabic_text.append(arabic_char)

        return ''.join(arabic_text)


if __name__ == '__main__':
    app = wx.App(False)
    frame = ArabicBrailleTranslator(None, title="مترجم برايل - Arabic Braille Translator")
    frame.Show()
    app.MainLoop()
