# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from subprocess import Popen, PIPE,STDOUT
import os
import sys
import unittest
import re
import ast

from dwave.cloud.utils import retried

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IntegrationTests(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    @retried(2)
    def test_factoring(self):
        demo_file = os.path.join(project_dir, 'demo.py')
        p = Popen([sys.executable, demo_file], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(b'49\n')
        output = p.communicate()[0]
        output = output.decode(encoding='UTF-8')
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n"+ output)

        best_line = re.search('^(\([^\n]*)', output, re.M).group(0)
        best_factors = re.search('(\([^a-z]*)', best_line, re.I).group(0)

        with self.subTest(msg="Verify output contains factor (7,7)"):
            self.assertEqual(ast.literal_eval(best_factors), (7,7))
        with self.subTest(msg="Verify output contains valid result"):
            self.assertIn("Yes", best_line)

if __name__ == '__main__':
    unittest.main()
