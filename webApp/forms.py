from django import forms

# class StudentInfoForm(forms.ModelForm):
#     class Meta:
#         model = StudentInfo
#         fields = "__all__"

'''
INSIDE THIS ARE CURRENTLY NOT IN USE AS I MIGRATE THEM IN TO OTHER APPS
-----BY SOUMMA-------------

class StudentInfoForm(forms.Form):
    Roll = forms.IntegerField(required = False)
    Name = forms.CharField(max_length=50,required = False)
    Sex = forms.ChoiceField(choices=StudentInfo.GenderList,required = False)
    Group = forms.ChoiceField(choices=StudentInfo.GroupList,required = False)
    Father_Name = forms.CharField(max_length=50,required = False)
    Mother_Name = forms.CharField(max_length=50,required = False)
    DOB = forms.DateField(required = False)
    Guardian_Mobile_No = forms.CharField(max_length=14,required = False)
    Session = forms.IntegerField(required = False)
    YearStatus = forms.ChoiceField(choices=StudentInfo.YearStatusList,required = False)
    Password = forms.CharField(max_length=150, widget=forms.PasswordInput,required = False)
    image = forms.ImageField(required = False)
    email = forms.EmailField(required = False)
    # def clean_picture(self):
    #     print("I am in")
    #     picture = self.cleaned_data.get('image')
    #     print(picture)
    #     if not picture:
    #         raise forms.ValidationError("No image!")
    #     else:
    #         w, h = get_image_dimensions(picture)
    #         if w < 100:
    #             raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 100px" % w)
    #         if h < 200:
    #             raise forms.ValidationError("The image is %i pixel high. It's supposed to be 200px" % h)
    #     return picture


'''
