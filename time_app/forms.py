from django import forms
from django.core import mail
from .models import Message,Group,Friend,Good
from django.contrib.auth.models import User

#Messageのフォーム__________________________________________________
class MessageForm(forms.ModelForm):
  class Meta:
    model = Message
    fields = ['owner', 'group', 'content']

#Groupのフォーム__________________________________________________
class GroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ['owner', 'title']

#Friendのフォーム__________________________________________________
class FriendForm(forms.ModelForm):
  class Meta:
    model = Friend
    fields = ['owner', 'user', 'group']

#Goodのフォーム__________________________________________________
class GoodForm(forms.ModelForm):
  class Meta:
    model = Good
    fields = ['owner', 'message']

#Groupのチェックフォーム__________________________________________________
class GroupCheckForm(forms.Form):
  def __init__(self, user, *args, **kwargs):
    super(GroupCheckForm, self).__init__(*args, **kwargs)
    public = User.objects.filter(username='public').first()
    self.fields['groups'] = forms.MultipleChoiceField(
      choices=[(item.title, item.title) for item in \
        Group.objects.filter(owner__in=[user, public])],
      widget=forms.CheckboxSelectMultiple(),
    )

#Groupの選択メニューフォーム__________________________________________________
class GroupSelectForm(forms.Form):
  def __init__(self, user, *args, **kwargs):
    super(GroupSelectForm, self).__init__(*args, **kwargs)
    self.fields['groups'] = forms.ChoiceField(
      choices=[('-','-')] + [(item.title, item.title) \
         for item in Group.objects.filter(owner=user)],
        widget=forms.Select(attrs={'class':'form-control'}),
    )
    
#Friendのチェックフォーム__________________________________________________
class FriendsForm(forms.Form):
  def __init__(self, user, friends=[], vals=[], *args, **kwargs):
    super(FriendsForm, self).__init__(*args, **kwargs)
    self.fields['friends'] = forms.MultipleChoiceField(
      choices=[(item.user, item.user) for item in friends],
      widget=forms.CheckboxSelectMultiple(),
      initial=vals
    )

# Group作成フォーム______________________________________________________
class CreateGroupForm(forms.Form):
  group_name = forms.CharField(max_length=50 ,\
    widget=forms.TextInput(attrs={'class':'form-control'}))

# 投稿フォーム___________________________________________________________
class PostForm(forms.Form):
  content = forms.CharField(max_length=500, \
    widget=forms.Textarea(attrs={'class':'form-control', 'row':2}))

  def __init__(self, user, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)
    public = User.objects.filter(username='public').first()
    self.fields['groups'] = forms.ChoiceField(
      choices=[('-', '-')] + [(item.title, item.title) \
        for item in Group.objects. \
        filter(owner__in = [user,public])],
        widget=forms.Select(attrs={'class':'form-control'}),
    )

# お問合せフォーム----------------------------------------------------------
from django.core.mail import EmailMessage, message

class ContactForm(forms.Form):
  name = forms.CharField(label='お名前')
  email = forms.EmailField(label='メールアドレス')
  title = forms.CharField(label='タイトル')
  contact_message = forms.CharField(label='メッセージ', widget=forms.Textarea)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['name'].widget.attrs['placeholder'] = \
    'お名前を入力してください'
    self.fields['name'].widget.attrs['class'] = 'form-control'

    self.fields['email'].widget.attrs['plaseholder'] = \
    'メールアドレスを入力してください'

    self.fields['email'].widget.attrs['class'] = 'form-control'

    self.fields['title'].widget.attrs['placeholder'] = \
    'タイトルを入力してください'
    self.fields['title'].widget.attrs['class'] = 'form-control'

    self.fields['contact_message'].widget.attrs['placeholder'] = \
    'メッセージを入力してください'
    self.fields['contact_message'].widget.attrs['class'] = 'form-control'

  def send_email(self):
    name = self.cleaned_data['name']
    email = self.cleaned_data['email']
    title = self.cleaned_data['title']
    contact_message = self.cleaned_data['contactmessage']

    subject = 'お問合せ: {}'.format(title)
    contact_message = \
    '送信者名: {0}¥nメールアドレス: {1}¥nタイトル: {2}¥nメッセージ:¥n{3}' \
      .format(name, email, title, contact_message)
    from_email = 'admin@example.com'
    to_list = ['takumu8311@gmail.com']
    contact_message = EmailMessage(subject = subject,
                                    body = contact_message,
                                    from_email = from_email,
                                    to = to_list,
                                    )
    contact_message.send()