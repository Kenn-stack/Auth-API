import string
import secrets



def _generate_digits(length):
    """
    Generate digits

    :param_length: The lemgth of the digits.
    :type length: int
    :return: The digits.
    :return_type str

    """
    digits = string.digits
    digits_without_zero = digits[1:]
    return ''.join(secrets.choice(digits if (i>0) else digits_without_zero) for i in range(length))



def _generate_hex(length):
    """
    Generate hexadecimal

    :param_length: The lemgth of the hexadecimal.
    :type length: int
    :return: The hex.
    :return_type str

    """
    hex = string.hexdigits
    hex_digits_without_zero = hex[1:]

    return ''.join(secrets.choice(hex if (i>0) else hex_digits_without_zero) for i in range(length))



def generate_OTP():
    return _generate_digits(6)


def generate_user_id(length):
    return _generate_hex(length)

