from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, Dict, List, Union

from .helpers.others import fake
from .classes.basic_test import Test
from .helpers.report import generate
from .classes.basic_case import TestCase
from .classes.basic_suite import TestSuite
from .classes.basic_group import TestGroup
from .helpers.others import FakePoolExecutor
from .classes.listeners.basic import Listener
from .classes.exc_thread import run_with_timeout
from .classes.listeners.default import DefaultListener
from .helpers.exception_traceback import exception_with_assert
from .exceptions import UnknownProviderName, TestIgnoredException, OnlyIfFailedException, SkipTestException

# Tests listener
_listener: Listener
# flag for running all test, sets to False to stop suite (when failed count reached)
_can_run = True
# maximum of fails for test in suite, if 0 then works till the end of tests
_max_fail = 0
# actual failed tests count
_actual_failed_count = 0

# Common parameters for whole test-suite
common_parameters: Dict[str, Any] = {}


def start(verbose: int = 0, listener: Listener = None, groups: List[str] = None, params: Dict[str, Any] = None,
          threads: int = 1, suite_name: str = 'Default Test Suite', dry_run: bool = False, filter_by_name: str = None,
          random_order: bool = False, max_fail: int = 0, generate_report: bool = False, **kwargs):
    """
    The main function of tests start

    :param suite_name: name of the test-suite
    :param listener: is test listener, DefaultListener is used by default. If set, then the verbose parameter is ignored
    (the one in the listener is used).
    :param verbose: is the report detail, 0 - briefly (only dots and 1 letter), 1 - detail, indicating only failed
    tests, 2 - detail, indicating successful and fallen, 3 - detail and at the end, a list of fallen and broken ones
    If not between 0 and 3, then 0 is accepted
    :param groups: is the list of group names to run, to run only the tests you need
    :param params: is the dictionary of parameters available in all tests (general run parameters)
    :param threads: is the number of threads to run tests by default is 1. Each group can run in a separate thread if
    necessary. This is an experimental feature and it can be useful only for tests NOT performing any complex
    calculations (CPU bound). It is best to use this parameter (more than 1) for tests related to the use of I / O
    operations - disk work, network requests. Obey the GIL!
    :param dry_run: if True runs test-suite with fake function except of real tests and fixtures, can be useful to
    find out order, number of tests, params of provider etc.
    :param filter_by_name if specified - runs only tests with name containing this parameter
    :param random_order if specified - runs tests inside each group in random order
    :param max_fail if greater than 0, than suite will stops, when reach that count of failed tests
    :param generate_report if specified - creates html report with the results in test folder
    :return: None
    """
    verbose = 0 if verbose not in range(4) else verbose
    if type(max_fail) is int and max_fail > 0:
        global _max_fail
        _max_fail = max_fail
    # If a listener is specified, then use it, otherwise by default
    global _listener
    _listener = listener if listener else DefaultListener(verbose)
    test_suite = TestSuite.get_instance()
    test_suite.name = suite_name
    if groups:
        test_suite.filter_groups(groups)
    if filter_by_name:
        test_suite.filter_tests(filter_by_name)
    # If there are no tests, then stop
    if test_suite.is_empty():
        _listener.on_empty_suite(test_suite)
        _listener.on_suite_ends(test_suite)
        if generate_report:
            generate(test_suite)
        return
    if params:
        common_parameters.update(params)
    if threads < 1:
        threads = 1
    # if there is only one test group no need more than 1 thread!
    if threads > 1 and len(test_suite.groups) <= 1:
        threads = 1
    if dry_run:
        _dry_run(test_suite)
    # Check if all used provider names are found
    _check_data_providers(test_suite)
    _run(test_suite, threads, random_order, generate_report)


def _dry_run(test_suite):
    """
    Clear all fixtures and replace real test with fake function
    :param test_suite: is TestSuite
    :return: None
    """
    _listener.on_dry_run(test_suite)
    test_suite.before = []
    test_suite.after = []
    for group in test_suite.groups.values():
        group.before = []
        group.after = []
        for test in group.tests:
            test.before = []
            test.after = []
            test.test = fake


def _run(test_suite: TestSuite, threads: int = 1, random_order: bool = False, generate_report: bool = False):
    for group in test_suite.groups.values():
        if random_order:
            group.shuffle_tests()
        else:
            group.sort_test_by_priority()
    # Create a pool of threads or fake pool to run tests, by default 1 thread execution
    pool = FakePoolExecutor() if threads <= 1 else ThreadPoolExecutor(max_workers=threads)
    test_suite.start_suite()
    _listener.on_suite_starts(test_suite)
    try:
        # If the fixture before the test suite has fallen, then will not run the tests (fixture after the test suite
        # will be executed with the appropriate flag)
        if not _run_before_suite(test_suite):
            return
        for group in test_suite.groups.values():
            # If there are no tests in the group, then skip it
            if not group.tests:
                continue
            pool.submit(_run_group_before_and_after_at_separate_thread, group)
        pool.shutdown(wait=True)
        _run_after(test_suite)
    finally:
        test_suite.stop_suite()
        _listener.on_suite_ends(test_suite)
        if generate_report:
            generate(test_suite)


def _run_group_before_and_after_at_separate_thread(group: TestGroup):
    # If the fixture before the group fell, then we do not run the tests
    if not _run_before_group(group):
        return
    _run_all_tests_in_group(group)
    _run_after(group)


def _run_before_suite(test_suite: TestSuite) -> bool:
    """
    Run fixtures before whole suite.
    :param test_suite: TestSuite
    :return: True if fixture is not fail, False otherwise
    """
    _run_before(test_suite)
    if test_suite.is_before_failed:
        _listener.on_before_suite_failed(test_suite)
        if test_suite.always_run_after:
            _run_after(test_suite)
        return False
    return True


def _run_before_group(group: TestGroup) -> bool:
    """
    Runs before group fixtures
    :param group: TestGroup
    :return: True if fixtures not failed, False otherwise
    """
    _run_before(group)
    if group.is_before_failed:
        for test in group.tests:
            test.stop(TestIgnoredException('Before module/group failed!'))
            _listener.on_ignored(test, 'before module/group')
        if group.always_run_after:
            _run_after(group)
        return False
    return True


def _run_test_with_provider(test):
    """
    Run test which has provider
    :param test: Test
    :return: None
    """
    test_suite = TestSuite.get_instance()
    provider = test.provider
    # If provider values is in the cache - get it from there
    generator = _provider_next(provider) if provider not in test_suite.cache else test_suite.cache[provider]
    try:
        is_any_value_provides = False
        need_to_cache = provider in test_suite.cached and provider not in test_suite.cache
        list_of_arguments = []
        for param in generator:
            is_any_value_provides = True
            if not _can_run:
                break
            clone = test.clone()
            clone.argument = param
            if need_to_cache:
                list_of_arguments.append(param)
            is_one_of_before_test_failed = _run_test_with_before_and_after(clone, False)
            if is_one_of_before_test_failed:
                _listener.on_before_provider_failed(test, provider)
                break
        # If no values at provider - ignore test
        if not is_any_value_provides:
            test.stop(TestIgnoredException(f'No values at provider {test.provider}'))
            _listener.on_ignored_with_provider(test)
        else:
            if need_to_cache:
                test_suite.cache[provider] = tuple(list_of_arguments)
    except TypeError as e:
        if 'is not iterable' not in e.args[0]:
            _listener.on_error_with_provider(provider, e)
            raise
        else:
            test.stop(TestIgnoredException(f'Error with provider {test.provider}'))
            _listener.on_ignored_with_provider(test)


def _run_all_tests_in_group(group: TestGroup):
    """
    Run all test of the group, after sorting them by priority
    :param group: TestGroup
    :return: None
    """
    is_one_of_before_test_failed = False
    for test in group.tests:
        if not _can_run:
            break
        if test.provider:
            _run_test_with_provider(test)
        else:
            is_one_of_before_test_failed = _run_test_with_before_and_after(test, is_one_of_before_test_failed)


def _run_test_with_before_and_after(test: Test, is_before_failed: bool) -> bool:
    if not is_before_failed:
        _run_before(test)
    else:
        test.is_before_failed = True
    if test.is_before_failed:
        test.stop(TestIgnoredException('Before test failed!'))
        _listener.on_ignored(test, 'before test')
        return True
    for retry in range(test.retries):
        clone = test.clone()
        if retry > 0:
            clone.name = clone.name + f' ({retry})'
        result = _run_test(clone)
        if result:
            break
    _run_after(test)
    return False


def _provider_next(provider_name: str) -> Any:
    """
    Gets provider functions return or yield(generator) and iterate it. If a close attribute exists (for files) try to
    close recourse after getting all elements.
    :param provider_name: name of the provider
    :return: generator
    """
    iter_ = TestSuite.get_instance().providers[provider_name][0]()
    for param in iter_:
        yield param
    # If it were file at provider - try to close it
    if hasattr(iter_, 'close'):
        try:
            iter_.close()
        except Exception as ex:
            _listener.on_error_with_provider(provider_name, exc=ex)
            # explicitly ignore, just notify our listener


def _run_test(test: Test) -> bool:
    """
    Run actual test
    :param test: Test (function to run)
    :return: True if test succeed, False otherwise
    """
    _listener.on_test_starts(test)
    try:
        if test.timeout:
            run_with_timeout(test)
        else:
            test.run()
        test.stop()
        _listener.on_success(test)
        return True
    except AssertionError as e:
        e = exception_with_assert(e)
        test.stop(e)
        _listener.on_failed(test, e)
        global _actual_failed_count
        if _max_fail and _actual_failed_count < _max_fail:
            _actual_failed_count += 1
        if _max_fail and _actual_failed_count >= _max_fail:
            global _can_run
            _can_run = False
            _listener.on_suite_stop_with_max_fail(_max_fail)
    except (TestIgnoredException, OnlyIfFailedException, SkipTestException, SystemExit) as e:
        test.stop(e)
        _listener.on_ignored_by_condition(test, e)
    except Exception as e:
        test.stop(e)
        _listener.on_broken(test, e)
    return False


def _check_data_providers(suite: TestSuite):
    """
    Checks if any test use data-provider, this provider is in collected list
    :param suite: TestSuite
    :return: None
    :raise UnknownProviderName if test uses name what is not in providers list
    """
    all_data_providers = [test.provider for group in suite.groups.values() for test in group.tests if test.provider]
    if not all_data_providers:
        return
    is_all_provider_known = all([provider in suite.providers for provider in all_data_providers])
    if not is_all_provider_known:
        name_ = [provider for provider in all_data_providers if provider not in suite.providers]
        raise UnknownProviderName(f'Cant find provider with name(s) {name_}. '
                                  f'You must have method with @data annotation in this package!')


def _run_before(test_case: Union[TestCase, TestSuite]):
    """
    Runs all fixtures before test case. If failed - set flaf is_before_failed to True
    :param test_case: Test or TestGroup
    :return: None
    """
    for before in test_case.before:
        result = _run_fixture(before, 'before', test_case.name)
        if result:
            test_case.is_before_failed = True


def _run_after(test_case: Union[TestCase, TestSuite]):
    """
    Runs all fixtures after test or group
    :param test_case: Test or TestGroup
    :return: None
    """
    if not test_case.always_run_after and test_case.is_before_failed:
        return
    for after in test_case.after:
        _run_fixture(after, 'after', test_case.name)


def _run_fixture(func: Callable, fixture_type: str, group_name: str) -> bool:
    """
    Runs fixture and returns result of the run
    :param func: fixture-function (marked @before etc.)
    :param fixture_type: type of the fixture to use in listener (before, after ...)
    :param group_name: name of the group
    :return: False if fixture not failed, True otherwise
    """
    is_failed: bool = False
    try:
        func()
    except Exception as error:
        _listener.on_fixture_failed(group_name, fixture_type, error)
        is_failed = True
    return is_failed
