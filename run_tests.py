#!/usr/bin/env python
"""
Test runner script for the Django project.
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Run the Django test suite."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    
    # List of test modules to run
    test_modules = [
        'core.tests.test_urls',
        # Add more test modules here as they are created
    ]
    
    failures = test_runner.run_tests(test_modules)
    sys.exit(bool(failures))

if __name__ == "__main__":
    run_tests()
