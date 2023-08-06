#!/usr/bin/env python
# Copyright (c) 2017 Vantiv eCommerce
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
from __future__ import absolute_import, division, print_function

import os
import sys
import tempfile

import six

package_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, package_root)

from cnpsdk import utils

def ask_user():
    attrs = [
        'username',
        'password',
        'merchant_id',
        'url',
        'proxy',
        'print_xml',
        'neuter_xml'
    ]
    attr_dict = {
        'username': '',
        'password': '',
        'merchant_id': '',
        'url': '',
        'proxy': '',
        'print_xml': 'n',
        'neuter_xml': 'n'
    }
    attr_valid_dict = {

        'neuter_xml': {
            'y': True,
            'n': False,
        },
        'print_xml': {
            'y': True,
            'n': False,
        }
    }
    attr_des_dict = {
        'username': 'Presenter Username for online request',
        'password': 'Presenter Password for online request',
        'merchant_id': 'Your merchant_id:',
        'url': 'URL for you online request',
        'proxy': 'If you want to using https proxy, please input your proxy server address. Must start with "https://"',
        'print_xml': 'Do you want to print xml in console? y for Yes, n for No.',
        'neuter_xml': 'Do you want to hide sensitive data in printed xml? y for Yes, n for No.'
    }
    print(CC.bpurple('Vantiv eCommerce Chargeback SDK configuration!'))
    print('''
Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).''')

    for attr in attrs:
        while True:
            print(gene_prompt(attr, attr_dict, attr_valid_dict, attr_des_dict))
            if six.PY3:
                x = input('')
            else:
                x = raw_input('')
            if not x:
                x = attr_dict[attr]
            if attr in attr_valid_dict:
                if x.lower() in attr_valid_dict[attr]:
                    x = attr_valid_dict[attr][x.lower()]
                else:
                    print('Invalid input for "%s" = "%s"' % (attr, x))
                    continue
            attr_dict[attr] = x
            break

    conf = utils.Configuration()
    for k in attr_dict:
        setattr(conf, k, attr_dict[k])
    print(CC.bgreen('Configurations have saved at: %s ' % conf.save()))
    print(CC.bpurple('Successful!'))


def gene_prompt(attr, attr_dict, attr_valid_dict, attr_des_dict):
    if attr_dict[attr]:
        if attr in attr_valid_dict:
            option_str = CC.bcyan('Please select from following options:\n')
            for k in attr_valid_dict[attr]:
                _opt = attr_valid_dict[attr][k]
                if isinstance(_opt, bool):
                    _opt = 'True' if _opt else 'False'
                option_str += '%s - %s\n' % (CC.bgreen(k), CC.byellow(_opt))

            prompt = '\n%s\n%s%s [%s]: ' % \
                     (CC.bcyan(attr_des_dict[attr]), option_str, CC.bred(attr), CC.bgreen(attr_dict[attr]))
        else:
            prompt = '\n%s\n%s [%s]: ' % (CC.bcyan(attr_des_dict[attr]), CC.bred(attr), attr_dict[attr])
    else:
        prompt = '\n%s\n%s: ' % (CC.bcyan(attr_des_dict[attr]), CC.bred(attr))
    return prompt


# noinspection PyClassHasNoInit
class CC:
    # RESET
    COLOR_OFF = '\033[0m'  # TEXT RESET

    # REGULAR COLORS
    BLACK = '\033[0;30m'  # BLACK
    RED = '\033[0;31m'  # RED
    GREEN = '\033[0;32m'  # GREEN
    YELLOW = '\033[0;33m'  # YELLOW
    BLUE = '\033[0;34m'  # BLUE
    PURPLE = '\033[0;35m'  # PURPLE
    CYAN = '\033[0;36m'  # CYAN
    WHITE = '\033[0;37m'  # WHITE

    # BOLD
    BBLACK = '\033[1;30m'  # BLACK
    BRED = '\033[1;31m'  # RED
    BGREEN = '\033[1;32m'  # GREEN
    BYELLOW = '\033[1;33m'  # YELLOW
    BBLUE = '\033[1;34m'  # BLUE
    BPURPLE = '\033[1;35m'  # PURPLE
    BCYAN = '\033[1;36m'  # CYAN
    BWHITE = '\033[1;37m'  # WHITE

    # UNDERLINE
    UBLACK = '\033[4;30m'  # BLACK
    URED = '\033[4;31m'  # RED
    UGREEN = '\033[4;32m'  # GREEN
    UYELLOW = '\033[4;33m'  # YELLOW
    UBLUE = '\033[4;34m'  # BLUE
    UPURPLE = '\033[4;35m'  # PURPLE
    UCYAN = '\033[4;36m'  # CYAN
    UWHITE = '\033[4;37m'  # WHITE

    @classmethod
    def black(cls, _str):
        return cls.BLACK + _str + cls.COLOR_OFF

    @classmethod
    def red(cls, _str):
        return cls.RED + _str + cls.COLOR_OFF

    @classmethod
    def green(cls, _str):
        return cls.GREEN + _str + cls.COLOR_OFF

    @classmethod
    def yellow(cls, _str):
        return cls.YELLOW + _str + cls.COLOR_OFF

    @classmethod
    def blue(cls, _str):
        return cls.BLUE + _str + cls.COLOR_OFF

    @classmethod
    def purple(cls, _str):
        return cls.PURPLE + _str + cls.COLOR_OFF

    @classmethod
    def cyan(cls, _str):
        return cls.CYAN + _str + cls.COLOR_OFF

    @classmethod
    def white(cls, _str):
        return cls.WHITE + _str + cls.COLOR_OFF

    @classmethod
    def ublack(cls, _str):
        return cls.UBLACK + _str + cls.COLOR_OFF

    @classmethod
    def ured(cls, _str):
        return cls.URED + _str + cls.COLOR_OFF

    @classmethod
    def ugreen(cls, _str):
        return cls.UGREEN + _str + cls.COLOR_OFF

    @classmethod
    def uyellow(cls, _str):
        return cls.UYELLOW + _str + cls.COLOR_OFF

    @classmethod
    def ublue(cls, _str):
        return cls.UBLUE + _str + cls.COLOR_OFF

    @classmethod
    def upurple(cls, _str):
        return cls.UPURPLE + _str + cls.COLOR_OFF

    @classmethod
    def ucyan(cls, _str):
        return cls.UCYAN + _str + cls.COLOR_OFF

    @classmethod
    def uwhite(cls, _str):
        return cls.UWHITE + _str + cls.COLOR_OFF

    @classmethod
    def bblack(cls, _str):
        return cls.BBLACK + _str + cls.COLOR_OFF

    @classmethod
    def bred(cls, _str):
        return cls.BRED + _str + cls.COLOR_OFF

    @classmethod
    def bgreen(cls, _str):
        return cls.BGREEN + _str + cls.COLOR_OFF

    @classmethod
    def byellow(cls, _str):
        return cls.BYELLOW + _str + cls.COLOR_OFF

    @classmethod
    def bblue(cls, _str):
        return cls.BBLUE + _str + cls.COLOR_OFF

    @classmethod
    def bpurple(cls, _str):
        return cls.BPURPLE + _str + cls.COLOR_OFF

    @classmethod
    def bcyan(cls, _str):
        return cls.BCYAN + _str + cls.COLOR_OFF

    @classmethod
    def bwhite(cls, _str):
        return cls.BWHITE + _str + cls.COLOR_OFF


def main(argv=sys.argv):
    ask_user()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
