import hug
import voluptuous


class Email(hug.types.Text):
    """E-mail string value"""

    def __call__(self, value):
        return voluptuous.Email()(super().__call__(value))


email = Email()
