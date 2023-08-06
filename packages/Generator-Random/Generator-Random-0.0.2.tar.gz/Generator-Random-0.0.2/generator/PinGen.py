import RandomHelper


def get_pin(pinlength=8):
    """Generates a random pin wiht the specified length"""
    pin_values = []
    count = 0
    while count < pinlength:
        pin_values.append(RandomHelper.singelton_int_bit(0, 9))
        count = count + 1

    generated_pin = ' '.join([str(value) for value in pin_values])
    return generated_pin
