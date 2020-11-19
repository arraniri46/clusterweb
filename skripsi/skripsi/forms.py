from django import forms

class FormField(forms.Form):
    jumlah_cluster = forms.IntegerField(
                            label='Masukkan jumlah cluster',
                            widget= forms.TextInput(
                                    attrs={
                                        'class' : 'form-control',
                                        'placeholder' : 'Rentang Cluster (2 s/d 8)',
                                        'type' : 'number',
                                        'min' : '2',
                                        'max' : '8'
                                    } 
                                )   
                            )

class UploadFileForm(forms.Form):
    file = forms.FileField()