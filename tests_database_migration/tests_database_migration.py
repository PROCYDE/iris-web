#  IRIS Source Code
#  Copyright (C) 2025 - DFIR-IRIS
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from unittest import TestCase
from pathlib import Path
import gzip
import tempfile
import shutil
from sqlalchemy import create_engine
from sqlalchemy import inspect

from test_harness.docker import Docker
from test_harness.iris import Iris

_IRIS_PATH = Path(__file__).parent.parent


class TestsDatabaseMigration(TestCase):

    def setUp(self) -> None:
        self._docker = Docker(_IRIS_PATH, 'docker-compose.dev.yml')

    def tearDown(self):
        self._docker.compose_down()
        self._docker.volume_rm('iris-web_db_data')

    @staticmethod
    def _extract_database_dump(name, destination_file):
        with gzip.open(f'database_dumps/{name}.gz', 'rb') as database_dump:
            shutil.copyfileobj(database_dump, destination_file)

    def _dump_database(self, name):
        with tempfile.TemporaryFile() as temporary_file:
            self._extract_database_dump(name, temporary_file)
            temporary_file.seek(0)
            self._docker.exec('iriswebapp_db', temporary_file, ['psql', '-U', 'postgres', '-d', 'iris_db'])

    def test_update_from_v2_4_14_should_not_fail(self):
        self._docker.compose_up('db')
        self._dump_database('v2.4.14_empty')
        self._docker.compose_up()

    def test_get_iocs_should_return_200_after_update_from_v2_4_22(self):
        self._docker.compose_up('db')
        self._dump_database('v2.4.22_empty')
        self._docker.compose_up()

        subject = Iris()
        case_identifier = subject.create_dummy_case()
        response = subject.get(f'/api/v2/cases/{case_identifier}/iocs')
        self.assertEqual(200, response.status_code)

    def test_update_from_v2_4_22_should_drop_table_ioc_links(self):
        self._docker.compose_up('db')
        self._dump_database('v2.4.22_empty')
        self._docker.compose_up()

        engine = create_engine('postgresql+psycopg2://postgres:__MUST_BE_CHANGED__@localhost:5432/iris_db')
        inspection = inspect(engine)
        logs = self._docker.extract_logs('app')
        self.assertNotIn('ioc_link', inspection.get_table_names(), logs)

    def test_update_from_v2_4_22_should_drop_table_ioc_links_when_there_is_an_ioc(self):
        self._docker.compose_up('db')
        self._dump_database('v2.4.22_with_ioc')
        self._docker.compose_up()

        engine = create_engine('postgresql+psycopg2://postgres:__MUST_BE_CHANGED__@localhost:5432/iris_db')
        inspection = inspect(engine)
        logs = self._docker.extract_logs('app')
        self.assertNotIn('ioc_link', inspection.get_table_names(), logs)
