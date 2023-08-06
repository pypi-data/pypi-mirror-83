from argparse import ArgumentParser
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    DATABASES={'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'orderable',
        'HOST': 'localhost'
    }},
    INSTALLED_APPS=(
        'orderable.tests',
    ),
    MIDDLEWARE_CLASSES=[],
)


django.setup()


if __name__ == "__main__":
    parser = ArgumentParser(description="Run the Django test suite.")
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_argument(
        '--noinput', action='store_false', dest='interactive', default=True,
        help='Tells Django to NOT prompt the user for input of any kind.')
    parser.add_argument(
        '--failfast', action='store_true', dest='failfast', default=False,
        help='Tells Django to stop running the test suite after first failed '
             'test.')
    parser.add_argument(
        '-k', '--keepdb', action='store_true', dest='keepdb', default=False,
        help='Tells Django to preserve the test database between runs.')
    parser.add_argument(
        '--reverse', action='store_true', default=False,
        help='Sort test suites and test cases in opposite order to debug '
             'test side effects not apparent with normal execution lineup.')
    parser.add_argument(
        '--debug-sql', action='store_true', dest='debug_sql', default=False,
        help='Turn on the SQL query logger within tests (Django 1.8+ only)')
    options = parser.parse_args()
    runner_kwargs = {
        'verbosity': options.verbosity,
        'interactive': options.interactive,
        'failfast': options.failfast,
        'keepdb': options.keepdb,
        'reverse': options.reverse,
    }
    runner_kwargs['debug_sql'] = options.debug_sql
    test_runner = DiscoverRunner(**runner_kwargs)
    failures = test_runner.run_tests(['orderable'])
    if failures:
        sys.exit(1)
