import getpass
import sys

import gkeepapi
import ptpython.repl


def main():
    user = input('Your Google user account name:\n')
    password = getpass.getpass('Your Google account password:\n')
    keep = gkeepapi.Keep()

    # TODO fix this. It's probably failing because of 2FA set up on my account.
    # The library worked at some point, I think, because I used it to check creation dates on some notes.
    # The error:
    # gkeepapi.exception.LoginException:
    # ('NeedsBrowser', 'To access your account, you must sign in on the web.
    # Touch Next to start browser sign-in.')
    #
    # Check out what's happening here https://github.com/kiwiz/gkeepapi/issues/81
    login_success = keep.login(user, password)
    if not login_success:
        sys.exit('Failed to log in to Google.')

    print('Google Keep API object is available as `keep`')
    ptpython.repl.embed(globals(), locals())


if __name__ == '__main__':
    main()
