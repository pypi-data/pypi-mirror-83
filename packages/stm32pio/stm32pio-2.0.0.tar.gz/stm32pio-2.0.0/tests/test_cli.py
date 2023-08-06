import configparser
import contextlib
import io
import pathlib
import re
import subprocess
import unittest.mock

# Provides test constants and definitions
from tests.common import *

import stm32pio.cli.app
import stm32pio.core.lib
import stm32pio.core.settings
import stm32pio.core.util


class TestCLI(CustomTestCase):
    """
    Some tests to mimic the behavior of end-user tasks (CLI commands such as 'new', 'clean', etc.). Run the main
    function passing the arguments to it but sometimes even run as subprocess (to capture actual STDOUT/STDERR output)
    """

    def test_clean(self):
        for case in ['--quiet', 'yes', 'no']:
            with self.subTest(case=case):
                # Create files and folders
                test_file = STAGE_PATH.joinpath('test.file')
                test_dir = STAGE_PATH.joinpath('test.dir')
                test_file.touch(exist_ok=False)
                test_dir.mkdir(exist_ok=False)

                # Clean ...
                if case == '--quiet':
                    return_code = stm32pio.cli.app.main(sys_argv=['clean', case, '-d', str(STAGE_PATH)],
                                                        should_setup_logging=False)
                else:
                    with unittest.mock.patch('builtins.input', return_value=case):
                        return_code = stm32pio.cli.app.main(sys_argv=['clean', '-d', str(STAGE_PATH)],
                                                            should_setup_logging=False)

                self.assertEqual(return_code, 0, msg="Non-zero return code")

                # ... look for remaining items ...
                if case == 'no':
                    with self.subTest():
                        self.assertTrue(test_file.is_file(), msg=f"{test_file} has been deleted")
                    with self.subTest():
                        self.assertTrue(test_dir.is_dir(), msg=f"{test_dir}/ has been deleted")
                else:
                    with self.subTest():
                        self.assertFalse(test_file.is_file(), msg=f"{test_file} is still there")
                    with self.subTest():
                        self.assertFalse(test_dir.is_dir(), msg=f"{test_dir}/ is still there")

                # ... and .ioc file should be preserved in any case
                with self.subTest():
                    self.assertTrue(STAGE_PATH.joinpath(f"{STAGE_PATH.name}.ioc").is_file(),
                                    msg="Missing .ioc file")

    def test_new(self):
        """
        Successful build is the best indicator that all went right so we use '--with-build' option here
        """
        return_code = stm32pio.cli.app.main(
            sys_argv=['new', '-d', str(STAGE_PATH), '-b', PROJECT_BOARD, '--with-build'],
            should_setup_logging=False)
        self.assertEqual(return_code, 0, msg="Non-zero return code")

        # .ioc file should be preserved
        self.assertTrue(STAGE_PATH.joinpath(f"{STAGE_PATH.name}.ioc").is_file(), msg="Missing .ioc file")

    def test_generate(self):
        return_code = stm32pio.cli.app.main(sys_argv=['generate', '-d', str(STAGE_PATH)], should_setup_logging=False)
        self.assertEqual(return_code, 0, msg="Non-zero return code")

        for directory in ['Inc', 'Src']:
            with self.subTest():
                self.assertTrue(STAGE_PATH.joinpath(directory).is_dir(), msg=f"Missing '{directory}'")
                self.assertNotEqual(len(list(STAGE_PATH.joinpath(directory).iterdir())), 0,
                                    msg=f"'{directory}' is empty")

        # .ioc file should be preserved
        self.assertTrue(STAGE_PATH.joinpath(f"{STAGE_PATH.name}.ioc").is_file(), msg="Missing .ioc file")

    def test_should_log_error(self):
        """
        We should see an error log message and a non-zero return code
        """
        with self.subTest(error="Incorrect path"):
            path_not_exist = pathlib.Path('path_some_uniq_name/does/not/exist')
            with self.assertLogs(level='ERROR') as logs:
                return_code = stm32pio.cli.app.main(sys_argv=['init', '-d', str(path_not_exist)],
                                                    should_setup_logging=False)
                self.assertNotEqual(return_code, 0, msg="Return code should be non-zero")
                # Actual text varies for different OSes and system languages so we check only for a part of the string
                self.assertTrue(next((True for msg in logs.output if 'path_some_uniq_name' in msg.lower()), False),
                                msg="'ERROR' logging message hasn't been printed")

        with self.subTest(error="No .ioc file"):
            dir_with_no_ioc_file = STAGE_PATH.joinpath('dir.with.no.ioc.file')
            dir_with_no_ioc_file.mkdir(exist_ok=False)
            with self.assertLogs(level='ERROR') as logs:
                return_code = stm32pio.cli.app.main(sys_argv=['init', '-d', str(dir_with_no_ioc_file)],
                                                    should_setup_logging=False)
                self.assertNotEqual(return_code, 0, msg="Return code should be non-zero")
                self.assertTrue(next((True for msg in logs.output if FileNotFoundError.__name__ in msg), False),
                                msg="'ERROR' logging message hasn't been printed")

    def test_verbosity(self):
        """
        Capture the full output. Check both the app logging messages and STM32CubeMX CLI output. Completely isolate
        runs by using subprocess

        Verbose logs format should match such a regex:
            ^(?=(DEBUG|INFO|WARNING|ERROR|CRITICAL) {0,4})(?=.{8} (?=(build|pio_init|...) {0,26})(?=.{26} [^ ]))

        Non-verbose:
            ^(?=(INFO) {0,4})(?=.{8} ((?!( |build|pio_init|...))))
        """

        # inspect.getmembers() is great but it triggers class properties to execute leading to the unwanted code
        # execution
        methods = dir(stm32pio.core.lib.Stm32pio) + ['main']

        with self.subTest(verbosity_level=stm32pio.core.util.Verbosity.NORMAL):
            result = subprocess.run([PYTHON_EXEC, STM32PIO_MAIN_SCRIPT, 'generate', '-d', str(STAGE_PATH)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

            self.assertEqual(result.returncode, 0, msg="Non-zero return code")
            # stderr and not stdout contains the actual output (by default for the logging module)
            self.assertNotIn('DEBUG', result.stderr, msg="Verbose logging output has been enabled on stderr")
            self.assertEqual(len(result.stdout), 0,
                             msg="Entire app output should flow through the logging module")

            regex = re.compile("^(?=(INFO) {0,4})(?=.{8} ((?!( |" + '|'.join(methods) + "))))", flags=re.MULTILINE)
            self.assertGreaterEqual(len(re.findall(regex, result.stderr)), 1,
                                    msg="Logs messages doesn't match the format")

            # The snippet of the actual STM32CubeMX output
            self.assertNotIn('Starting STM32CubeMX', result.stderr, msg="STM32CubeMX has printed its logs")

        with self.subTest(verbosity_level=stm32pio.core.util.Verbosity.VERBOSE):
            result = subprocess.run([PYTHON_EXEC, STM32PIO_MAIN_SCRIPT, '-v', 'new', '-d', str(STAGE_PATH),
                                     '-b', PROJECT_BOARD], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding='utf-8')

            self.assertEqual(result.returncode, 0, msg="Non-zero return code")
            # stderr and not stdout contains the actual output (by default for the logging module)
            self.assertEqual(len(result.stdout), 0,
                             msg="Process has printed something directly into STDOUT bypassing logging")
            self.assertIn('DEBUG', result.stderr, msg="Verbose logging output hasn't been enabled on STDERR")

            # Inject all methods' names in the regex. Inject the width of field in a log format string
            regex = re.compile("^(?=(DEBUG) {0,4})(?=.{8} (?=(" + '|'.join(methods) + ") {0," +
                               str(stm32pio.core.settings.log_fieldwidth_function) + "})(?=.{" +
                               str(stm32pio.core.settings.log_fieldwidth_function) + "} [^ ]))", flags=re.MULTILINE)
            self.assertGreaterEqual(len(re.findall(regex, result.stderr)), 1,
                                    msg="Logs messages doesn't match the format")

            # The snippet of the actual STM32CubeMX output
            self.assertIn("Starting STM32CubeMX", result.stderr, msg="STM32CubeMX has not printed its logs")

    def test_init(self):
        """
        Check for the config creation and parameters presence
        """
        result = subprocess.run([PYTHON_EXEC, STM32PIO_MAIN_SCRIPT, 'init', '-d', str(STAGE_PATH),
                                 '-b', PROJECT_BOARD], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.assertEqual(result.returncode, 0, msg="Non-zero return code")

        self.assertTrue(STAGE_PATH.joinpath(stm32pio.core.settings.config_file_name).is_file(),
                        msg=f"{stm32pio.core.settings.config_file_name} file hasn't been created")

        config = configparser.ConfigParser(interpolation=None)
        config.read(str(STAGE_PATH.joinpath(stm32pio.core.settings.config_file_name)))
        for section, parameters in stm32pio.core.settings.config_default.items():
            for option, value in parameters.items():
                with self.subTest(section=section, option=option,
                                  msg="Section/key is not found in the saved config file"):
                    self.assertIsNotNone(config.get(section, option, fallback=None))
        self.assertEqual(config.get('project', 'board', fallback="Not found"), PROJECT_BOARD,
                         msg="'board' has not been set")

    def test_status(self):
        """
        Test the app output returned as a response to the 'status' command
        """

        buffer_stdout = io.StringIO()
        with contextlib.redirect_stdout(buffer_stdout), contextlib.redirect_stderr(None):
            return_code = stm32pio.cli.app.main(sys_argv=['status', '-d', str(STAGE_PATH)], should_setup_logging=False)

        self.assertEqual(return_code, 0, msg="Non-zero return code")

        matches_counter = 0
        last_stage_pos = -1
        for stage in stm32pio.core.lib.ProjectStage:
            if stage != stm32pio.core.lib.ProjectStage.UNDEFINED:
                match = re.search(r"^((\[ \])|(\[\*\])) {2}" + str(stage) + '$', buffer_stdout.getvalue(), re.MULTILINE)
                self.assertTrue(match, msg="Status information was not found on STDOUT")
                if match:
                    matches_counter += 1
                    self.assertGreater(match.start(), last_stage_pos, msg="The order of stages is messed up")
                    last_stage_pos = match.start()

        self.assertEqual(matches_counter, len(stm32pio.core.lib.ProjectStage) - 1)  # UNDEFINED stage should not be printed
