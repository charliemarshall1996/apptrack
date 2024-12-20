"""Contains forms for the target app.

This module contains the forms for the target app. The TargetUpdateForm is used to 
update the target amount in the target update page.
"""

from django import forms

from .models import Target


class TargetUpdateForm(forms.ModelForm):
    """Form for updating the target amount.

    This form is used to update the target amount in the target update page.
    """

    class Meta:
        """Meta class for TargetUpdateForm.

        This class defines the model and fields for the form.

        Attributes:
            model (class): The model class for the form.
            fields (list): The list of fields to include in the form.
        """
        model = Target
        fields = ["amount"]

    def save(self, *args, **kwargs):
        """Saves the target instance with the given data without committing to the db.

        Returns:
            Target: the saved target instance
        """
        return super().save(*args, commit=False, **kwargs)
