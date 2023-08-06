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

import logging.config
import os
import random
import unittest
import uuid

from marquez_client import Clients
from marquez_client.models import (DatasetType, JobType)
from marquez_client.utils import Utils

_NAMESPACE = 'default'

log = logging.getLogger(__name__)


class TestAirflowDAG(unittest.TestCase):
    def setUp(self):
        log.debug("TestAirflowDAG.setup(): ")

        os.environ['MARQUEZ_BACKEND'] = 'file'
        self.client_wo_file = Clients.new_write_only_client()
        log.info("created marquez_client.")

    def test_create_dag(self):
        log.debug("TestAirflowDAG::test_create_dag")

        for i in range(1000):
            NAMESPACE = "my-namespace"
            OWNER = "me"
            SOURCE = "my-source"
            DATASET = f'my-dataset-{i}'
            PHYSICAL = f'public.my_table-{i}'
            run_id = str(uuid.uuid4())
            JOB = f'my-job-{i%10}'

            self.client_wo_file.create_namespace(NAMESPACE, OWNER)
            self.client_wo_file.create_source(
                SOURCE,
                'POSTGRESQL',
                "jdbc:postgresql://localhost:5432/test?user=fred&ssl=true")
            self.client_wo_file.create_dataset(
                NAMESPACE, DATASET, DatasetType.DB_TABLE,
                PHYSICAL, SOURCE, run_id)
            self.client_wo_file.create_job(NAMESPACE, JOB, JobType.BATCH)
            self.client_wo_file.create_job_run(NAMESPACE, JOB, run_id,
                                               mark_as_running=True)

            udiff = (i % 10 - random.randrange(10))

            if udiff >= -1 or udiff <= 1:
                self.client_wo_file.mark_job_run_as_failed(
                    run_id, Utils.utc_now())
            else:
                self.client_wo_file.mark_job_run_as_completed(
                    run_id, Utils.utc_now())


if __name__ == '__main__':
    unittest.main()
