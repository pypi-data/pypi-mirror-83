#  Copyright 2013-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import datetime
import logging
import mimetypes
import os
import re
from robot.api import ExecutionResult


logging.basicConfig()


class RobotResultsParser(object):

    def __init__(self, reporter, verbose=False):
        self._logger = logging.getLogger('Parser')
        if verbose:
            self._logger.setLevel(verbose)
        self.reporter = reporter
        self.start_time = None
        self.end_time = None
        self.base_dir = ''

    def xml_to_db(self, xml_file, base_dir=''):
        self._logger.info('- Parsing %s' % xml_file)
        self.base_dir = base_dir
        test_run = ExecutionResult(xml_file, include_keywords=True)

        self._find_start_end_time(test_run.suite)

        self._parse_suite(test_run.suite)

    def _find_start_end_time(self, suite):
        self.start_time = self._find_start_time(suite)
        self.end_time = self._find_end_time(suite)

    def _find_start_time(self, suite):
        if suite.starttime:
            return suite.starttime
        if suite.suites:
            return self._find_start_time(suite.suites[0])
        if suite.tests:
            return suite.tests[0].starttime
        if suite.keywords:
            return suite.keywords[0].starttime

    def _find_end_time(self, suite):
        if suite.endtime:
            return suite.endtime
        if suite.suites:
            return self._find_end_time(suite.suites[-1])
        if suite.tests:
            return suite.tests[-1].starttime
        if suite.keywords:
            return suite.keywords[-1].starttime

    def _timestamp(self, t_str):
        return int(datetime.datetime.strptime(t_str, '%Y%m%d %H:%M:%S.%f').timestamp() * 1000)

    def _parse_suite(self, suite):
        self._logger.info('`--> Parsing suite: %s' % suite.name)

        attributes = {
            'id': suite.id,
            'longname': suite.longname,
            'doc': suite.doc,
            'metadata': suite.metadata,
            'source': suite.source,
            'suites': suite.suites,
            'tests': suite.tests,
            'totaltests': suite.test_count,
            'starttime': self._timestamp(suite.starttime or self.start_time),
            'endtime': self._timestamp(suite.endtime or self.end_time),
            'status': suite.status,
            'statistics': suite.statistics,
            'message': suite.message,
        }

        self.reporter.start_suite(suite.name, attributes)

        self._parse_suites(suite)
        self._parse_tests(suite.tests)
        self._parse_keywords(suite.keywords)

        self.reporter.end_suite(suite.name, attributes)
        if suite.id == 's1' and not suite.suites:
            attributes['id'] = suite.id
            self.reporter.end_suite(suite.name, attributes)

    def _parse_suites(self, suite):
        [self._parse_suite(subsuite) for subsuite in suite.suites]

    def _parse_tests(self, tests):
        [self._parse_test(test) for test in tests]

    def _parse_test(self, test):
        self._logger.info('  `--> Parsing test: %s' % test.name)

        attributes = {
            'id': test.id,
            'longname': test.longname,
            'doc': test.doc,
            'tags': [tag for tag in test.tags],
            'critical': test.critical,
            'template': '',
            'starttime': self._timestamp(test.starttime),
            'endtime': self._timestamp(test.endtime),
            'status': test.status,
            'message': test.message
        }

        self.reporter.start_test(test.name, attributes)

        self._parse_keywords(test.keywords)

        self.reporter.end_test(test.name, attributes)

    def _parse_keywords(self, keywords):
        [self._parse_keyword(keyword) for keyword in keywords]

    def _parse_keyword(self, keyword):
        self._logger.debug('    `--> Parsing keyword: %s' % keyword.name)

        attributes = {
            'type': keyword.type,
            'kwname': keyword.kwname,
            'libname': keyword.libname,
            'doc': keyword.doc,
            'args': keyword.args,
            'assign': keyword.assign,
            'tags': keyword.tags,
            'starttime': self._timestamp(keyword.starttime),
            'endtime': self._timestamp(keyword.endtime),
            'status': keyword.status
        }

        self.reporter.start_keyword(keyword.name, attributes)

        self._parse_messages(keyword.messages)
        self._parse_keywords(keyword.keywords)

        self.reporter.end_keyword(keyword.name, attributes)

    def _parse_messages(self, messages):
        for message in messages:
            self._logger.debug('      `--> Parsing log: %s' % message.message)
            result = re.search(r'<a href=.+?><img src=\"(.+?)\".*?><\/a>', message.message)
            if result:
                image_file = result.group(1)
                self._logger.debug('      `----> Send image file: %s' % image_file)
                file_path = os.path.join(self.base_dir, image_file)
                with open(file_path, 'rb') as f:
                    attachment = {'name': image_file, 'data': f.read(),
                                  'mime': mimetypes.guess_type(file_path)[0] or 'image/png'}
                    self.reporter.log_message({'message': message.message, 'level': message.level,
                                               'timestamp': self._timestamp(message.timestamp),
                                               'html': message.html, 'attachment': attachment})
            else:
                self.reporter.log_message({'message': message.message, 'level': message.level,
                                           'timestamp': self._timestamp(message.timestamp), 'html': message.html})
