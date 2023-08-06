"""
Copyright (C) Kehtra Pty Ltd - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from functools import wraps
from datetime import datetime


def refresh_token(func):
    """
    Decorator to refresh the currently issued token if
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # log user in if expiry delta exceeded then execute function
        now = datetime.now()
        if (self.expiry - datetime.now()).total_seconds() < self.expiry_delta:
            self.logon()
        return func(self, *args, **kwargs)

    return wrapper
