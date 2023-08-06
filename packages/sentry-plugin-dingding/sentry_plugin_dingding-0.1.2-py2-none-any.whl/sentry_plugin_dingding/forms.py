# coding: utf-8
from django import forms
from valueDict import defaultMarkdown, markdownMap
class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DingTalk robot access_token',
    )
    customer_markdown = forms.CharField(
        widget=forms.Textarea(attrs={u"rows": 5, u"class": u"span9"}),
        initial=defaultMarkdown,
        help_text=u'''自定义markdown格式，\n支持变量：\n{var}'''.format(var='\n'.join(markdownMap.keys())),
        label=u"自定义内容",
        required=False,
    )
