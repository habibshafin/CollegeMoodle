from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    #10485760
    if filesize > 4000:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value