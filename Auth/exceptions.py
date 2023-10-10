from rest_framework.exceptions import APIException

class PasswordNotSaved(APIException):
    status_code = 500
    default_detail = 'Could not save Password to database'
    default_code = 'not_saved'


class OTPNotMatchedException(APIException):
    status_code = 400
    default_detail = 'OTP does not match'
    default_code = 'not_matched' 