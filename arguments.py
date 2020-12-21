from argparse import ArgumentParser


class Arguments:
    @staticmethod
    def parse():
        parser = ArgumentParser()

        parser.add_argument('-s', '--secret',
                            required=True,
                            help='The JWT secret key to use')

        parser.add_argument('-e', '--email',
                            required=True,
                            help='The email address to use for confirmations')

        parser.add_argument('-p', '--password',
                            required=True,
                            help='The password of the email address')

        return parser.parse_args()
