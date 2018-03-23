from django.core.management import call_command
from django_extensions.management.commands.shell_plus import Command as ShellPlus


class Command(ShellPlus):
    help = (
        'for development'
        'sqlite の オンメモリデータベースなどの際に、'
        '毎回 migrate をしなくて良くなる'
        )

    def handle(self, *args, **options):
        call_command('migrate')
        super().handle(*args, **options)
