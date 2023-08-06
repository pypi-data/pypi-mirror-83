from utilities.choices import ChoiceSet

class InternalOnlyChoices(ChoiceSet):
    INTERNAL_ONLY_YES = True
    INTERNAL_ONLY_NO = False
    
    CHOICES = (
        (INTERNAL_ONLY_YES, 'true'),
        (INTERNAL_ONLY_NO, 'false')
    )
