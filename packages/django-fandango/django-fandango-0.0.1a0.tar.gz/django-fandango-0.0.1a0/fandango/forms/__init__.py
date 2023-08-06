from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


def get_default_form_helper(submit_text, inline=False, method="POST"):
    helper = FormHelper()
    helper.add_input(Submit('submit', submit_text, css_class="loading-button"))
    helper.form_method = method
    if inline:
        helper.form_class = 'form-inline'
    return helper
