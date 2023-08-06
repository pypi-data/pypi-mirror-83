MODULE_NAME_BANNER = """       █████████                                                    █████                      
  ███░░░░░███                                                  ░░███                       
 ███     ░░░   ██████  ████████    ██████  ████████   ██████   ███████    ██████  ████████ 
░███          ███░░███░░███░░███  ███░░███░░███░░███ ░░░░░███ ░░░███░    ███░░███░░███░░███
░███    █████░███████  ░███ ░███ ░███████  ░███ ░░░   ███████   ░███    ░███ ░███ ░███ ░░░ 
░░███  ░░███ ░███░░░   ░███ ░███ ░███░░░   ░███      ███░░███   ░███ ███░███ ░███ ░███     
 ░░█████████ ░░██████  ████ █████░░██████  █████    ░░████████  ░░█████ ░░██████  █████    
  ░░░░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░      ░░░░░░░░    ░░░░░   ░░░░░░  ░░░░░     



                                                                                                 """
COMPANY_NAME = """████████╗███████╗ ██████╗██╗  ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ██╗  ██╗██╗   ██╗████████╗███████╗
╚══██╔══╝██╔════╝██╔════╝██║  ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗██║  ██║╚██╗ ██╔╝╚══██╔══╝██╔════╝
   ██║   █████╗  ██║     ███████║██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║ ╚████╔╝    ██║   █████╗  
   ██║   ██╔══╝  ██║     ██╔══██║██║╚██╗██║██╔══╝  ██║   ██║██╔═══╝ ██╔══██║  ╚██╔╝     ██║   ██╔══╝  
   ██║   ███████╗╚██████╗██║  ██║██║ ╚████║███████╗╚██████╔╝██║     ██║  ██║   ██║      ██║   ███████╗
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝
                                                                                                      """
AUTHOR_NAME = """  ABHIJEET SRIVASTAV"""

"""----------------------------------------------------------------------------------------------------------------"""

"""Generator provides methods which allows to generate:
    -->First Western Name
    -->Last Western Name
    -->Full Western Name
    -->Numeric Password
    -->Alphabetic Password
    -->Alpha Numeric Password
    -->Alpha Numeric Special Password
    -->Pin
    -->IPV4 Address
    -->IPV6 Address
    --MAC Address
    -->Email Address"""

version = '1.0.0 (Oct 19 2020, 00:16:47) [MSC v.1916 64 bit (AMD64)]'

"""----------------------------------------------------------------------------------------------------------------"""

__allmodules__ = ["NameGen", "PassGen", "PinGen", "RandomHelper", "SystemGen", "EmailGen"]

__allmethodsavailable__ = ["get_first_name_western", "get_last_name_western", "get_full_name_western", "get_pass_num",
                           "get_pass_alpha", "get_pass_alphanum", "get_pass_aplhanumspecial", "get_pin", "get_ipv4",
                           "get_mac", "get_ipv6", "get_email"]

__allexistingmethods__ = ["get_name", "get_first_name_western", "get_last_name_western", "get_full_name_western",
                          "get_pass_unit", "pass_maker", "get_pass_num",
                          "get_pass_alpha", "get_pass_alphanum", "get_pass_aplhanumspecial", "get_pin", "get_ipv4",
                          "get_mac", "get_ipv6", "_lastbit", "_getrandbits", "_randbelow", "singelton_int_bit",
                          "from_bytes", "singelton_float_bit", "get_email_unit", "get_email"]

try:
    from NameGen import get_first_name_western, get_last_name_western, get_full_name_western
except ModuleNotFoundError:
    print('No module named NameGen found')

try:
    from PassGen import get_pass_num, get_pass_alpha, get_pass_alphanum, get_pass_aplhanumspecial
except ModuleNotFoundError:
    print('No module named PassGen found')

try:
    from PinGen import get_pin
except ModuleNotFoundError:
    print('No module named PinGen found')

try:
    from SystemGen import get_ipv4, get_mac, get_ipv6
except ModuleNotFoundError:
    print('No module named SystemGen found')


# Miscallaneous Methods
def introduce_self():
    print('Presenting:-', '\n\n', MODULE_NAME_BANNER, '\n\n' + 'All Rights Reserved By:-', '\n', COMPANY_NAME,
          '\n\n\n' + 'Written By:-',
          AUTHOR_NAME, '\n\n\n')


if __name__ == '__main__':
    introduce_self()
