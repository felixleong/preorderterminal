from preorder.config import USERS
import hug


def __verify_user(user_name, password):
    """
    Verifies the user.

    :param str user: The username.
    :param str password: The password.
    :returns: Either the username as a string or False if the authentication
        fails.
    """
    if user_name in USERS and password == USERS[user_name]:
        return user_name

    return False


http_basic_auth = hug.authentication.basic(__verify_user)
