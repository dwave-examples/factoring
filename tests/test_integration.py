#    Copyright 2020 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from subprocess import Popen, PIPE,STDOUT
import unittest
import time
import os

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []

    def VerifyErrors(self,output):

        try: 
            self.assertNotIn("ERROR",output.upper() )
        except AssertionError as e:
            print("Verify if error string contains in output failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertNotIn("WARNING",output.upper() )
        except AssertionError as e:
            print("Verify if warning string contains in output failed \n")
            self.verificationErrors.append(str(e))

    def test_factoring(self):
        cwd=os.getcwd()
        p = Popen(["python",  cwd+"/demo.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
        p.stdin.write(b'49\n')
        time.sleep(5)
        output = p.communicate()[0]
        output=str(output)
        print("Example output \n"+output)
        os.chdir(cwd)

        try: 
            self.assertIn("'results': [{'a': 7,".upper(),output.upper() )
        except AssertionError as e:
            print("Verification failed :- verify if output contains 'results': [{'a': 7, \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertIn("'b': 7,".upper(),output.upper() )
        except AssertionError as e:
            print("Verification failed :- Verify if output contains 'b': 7 \n")
            self.verificationErrors.append(str(e))

        self.VerifyErrors(output)

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()