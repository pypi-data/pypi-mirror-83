import RandomHelper


def get_ipv4():
    """Generates a random IPV4 address the specified length"""
    IPV4_LENGTH = 10
    ip_unit_value = []
    count = 0
    while count < IPV4_LENGTH:
        ip_unit_value.append(RandomHelper.singelton_int_bit(0, 9))
        count = count + 1

    generated_address = '{0}{1}{2}.{3}{4}{5}.{6}{7}.{8}{9}'.format(ip_unit_value[0], ip_unit_value[1], ip_unit_value[2],
                                                                   ip_unit_value[3], ip_unit_value[4], ip_unit_value[5],
                                                                   ip_unit_value[6], ip_unit_value[7], ip_unit_value[8],
                                                                   ip_unit_value[9])
    return generated_address


def get_ipv6():
    """Generates a random IPV6 address the specified length"""
    IPV6_LENGTH = 16 ** 4
    generated_address = ":".join(("%x" % RandomHelper.singelton_int_bit(0, IPV6_LENGTH) for i in range(8)))
    return generated_address


def get_mac():
    """Generates a random MAC address the specified length"""
    MAC_LENGTH = 16 ** 2
    generated_mac = "-".join(("%x" % RandomHelper.singelton_int_bit(0, MAC_LENGTH) for i in range(6)))
    return generated_mac

