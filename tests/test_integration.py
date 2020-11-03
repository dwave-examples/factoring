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

from dwave.cloud.utils import retried

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IntegrationTests(unittest.TestCase):

    @retried(2)
    def test_factoring(self):
        demo_file = os.path.join(project_dir, 'demo.py')
        p = Popen([sys.executable, demo_file], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(b'49\n')
        output = p.communicate()[0]
        output = output.decode(encoding='UTF-8').upper()
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n"+ output)

        best_start = output.find("OCCURRENCES")
        best_end = max(output.find("OCCURRENCES", best_start+1),
                              len(output))  # For the rare case of one solution
        best = output[best_start:best_end-1]

        with self.subTest(msg="Verify if output contains result a==7"):
            self.assertIn("'A': 7", best)
        with self.subTest(msg="Verify if output contains result b==7"):
            self.assertIn("'B': 7", best)
        with self.subTest(msg="Verify if output contains valid result"):
            self.assertIn("VALID", best)
        with self.subTest(msg="Verify if error string contains in output"):
            self.assertNotIn("ERROR", output)
        with self.subTest(msg="Verify if warning string contains in output"):
            self.assertNotIn("WARNING", output)

if __name__ == '__main__':
    unittest.main()
