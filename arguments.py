from argparse import ArgumentParser


class Arguments:
    @staticmethod
    def parse():
        parser = ArgumentParser()

        parser.add_argument('-s', '--secret',
                            required=True,
                            help='The JWT secret key to use')

        return parser.parse_args()
