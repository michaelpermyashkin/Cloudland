from django import forms
from .models import ProductReview

class ContactForm(forms.Form):
    your_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['product', 'user', 'rating', 'subject', 'comment']

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({
            'label': 'subject',
            'class': 'form-control',
            'placeholder': 'Add a review headline',
            'type': 'text'})
        self.fields['comment'].widget.attrs.update({
            'label': 'comment',
            'placeholder': 'What would you like others to know about this item?',
            'class': 'form-control',
            'type': 'text'})