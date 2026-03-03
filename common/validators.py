from django.core.exceptions import ValidationError
from datetime import date

def validate_birth_date(value):
    if value == None:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Возраст пользователя должен достигать 18 и более!")
    
    return value
