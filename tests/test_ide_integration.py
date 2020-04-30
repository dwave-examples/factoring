#    Copyright 2018 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
# import pytest
import logging
import os
from subprocess import Popen, PIPE,STDOUT
import inspect
import time

# These are integration tests with leap ide
# This require loding leap ide docker image and run inside that image
class LeapIdeIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        self.logger = None
        self.log = self.custom_logger(logging.DEBUG)

    def custom_logger(self,log_level=logging.DEBUG):

        # Check if logger object exists
        if self.logger is not None:
            return self.logger

        # Gets the name of the class / method from where this method is called
        logger_name = inspect.stack()[1][3]
        self.logger = logging.getLogger(logger_name)

        # By default, log all messages
        self.logger.setLevel(logging.DEBUG)

        # Get log file name from environment getting set in testRunner.sh
        log_file= os.getcwd()+"logs.log"
        if os.getenv('log_file') is not None and os.getenv('log_file'):
            log_file = os.environ['log_file']

        # File handler for logging
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        self.logger.addHandler(console_handler)

        return self.logger

    def VerifyErrors(self,output):

        try: 
            self.assertNotIn("ERROR",output.upper() )
            self.log.info("Verify if error string contains in output successful \n")
        except AssertionError as e:
            self.log.error("Verify if error string contains in output failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertNotIn("WARNING",output.upper() )
            self.log.info("Verify if warning string contains in output successful \n")
        except AssertionError as e:
            self.log.error("Verify if warning string contains in output failed \n")
            self.verificationErrors.append(str(e))

    def test_factoring(self):
        cwd=os.getcwd()
        # os.chdir(cwd+"")
        p = Popen(["python",  cwd+"/demo.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
        p.stdin.write(b'49\n')
        time.sleep(5)
        output = p.communicate()[0]
        output=str(output)
        self.log.info("Example output \n"+output)
        os.chdir(cwd)

        try: 
            self.assertIn("'results': [{'a': 7,".upper(),output.upper() )
            self.log.info("Test factoring example verification successful \n")
        except AssertionError as e:
            self.log.error("Test factoring example verification failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertIn("'b': 7,".upper(),output.upper() )
            self.log.info("Test factoring example verification successful \n")
        except AssertionError as e:
            self.log.error("Test factoring example verification failed \n")
            self.verificationErrors.append(str(e))

        self.VerifyErrors(output)

