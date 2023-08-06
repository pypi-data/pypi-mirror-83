# -*- encoding: utf-8 -*-
# pass import - Passwords importer swiss army knife
# Copyright (C) 2017-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import json

from pass_import.formats.json import JSON


class OTP(JSON):
    """Base class for OTP based importers."""
    content = ''

    # Import methods

    @staticmethod
    def _otp(item):
        otp = "otpauth://%s/totp-secret?" % item.get('type', 'totp').lower()
        otp += "secret=%s&issuer=%s" % (item['secret'], item['label'])
        for setting in ['algorithm', 'digits', 'counter', 'period']:
            if setting in item:
                otp += "&%s=%s" % (setting, item[setting])
        return otp

    def parse(self):
        """Parse OTP based file."""
        jsons = json.loads(self.content)
        for item in jsons:
            entry = dict()
            entry['title'] = item['label']
            entry['otpauth'] = self._otp(item)

            for key in ['type', 'thumbnail', 'last_used']:
                entry[key] = str(item.get(key, '')).lower()
            entry['tags'] = ', '.join(item['tags'])
            self.data.append(entry)

    # Context manager method

    def open(self):
        """Parse OTP based file."""
        super(OTP, self).open()
        self.content = self.file.read()
