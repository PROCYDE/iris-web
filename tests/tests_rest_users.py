#  IRIS Source Code
#  Copyright (C) 2023 - DFIR-IRIS
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
from iris import Iris
from iris import ADMINISTRATOR_USER_IDENTIFIER
from iris import IRIS_CASE_ACCESS_LEVEL_FULL_ACCESS
from iris import IRIS_PERMISSION_SERVER_ADMINISTRATOR
from iris import IRIS_PERMISSION_ALERTS_WRITE

_IDENTIFIER_FOR_NONEXISTENT_OBJECT = 123456789


class TestsRestUsers(TestCase):

    def setUp(self) -> None:
        self._subject = Iris()

    def tearDown(self):
        self._subject.clear_database()

    def test_get_users_should_return_200(self):
        response = self._subject.get('/manage/users/list')
        self.assertEqual(200, response.status_code)

    def test_get_users_should_return_403_for_user_without_rights(self):
        user = self._subject.create_dummy_user()
        response = user.get('/manage/users/list')
        self.assertEqual(403, response.status_code)

    def test_create_user_should_return_201(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body)
        self.assertEqual(201, response.status_code)

    def test_create_user_should_return_user_name(self):
        user_name = 'user_test'
        body = {
            'user_name': user_name,
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        self.assertEqual(user_name, response['user_name'])

    def test_create_user_should_return_user_email(self):
        user_email = 'new_user_email'
        body = {
            'user_name': 'user_test',
            'user_login': 'new_user_login',
            'user_email': user_email,
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        self.assertEqual(user_email, response['user_email'])

    def test_create_user_should_return_user_is_service_account(self):
        user_is_service_account = True
        body = {
            'user_name': 'user_test',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': user_is_service_account,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        self.assertEqual(user_is_service_account, response['user_is_service_account'])

    def test_create_user_should_set_in_dark_mode(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_isadmin': True,
            'in_dark_mode': True
        }
        response = self._subject.create('/api/v2/manage/users', body)
        self.assertEqual(201, response.status_code)

    def test_create_user_should_return_400_when_user_name_field_is_missing(self):
        body = {
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body)
        self.assertEqual(400, response.status_code)

    def test_create_user_should_return_400_when_user_name_is_not_a_string(self):
        body = {
            'user_name': 12345,
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body)
        self.assertEqual(400, response.status_code)

    def test_create_user_should_return_403_when_user_has_no_permission_to_create_user(self):
        user = self._subject.create_dummy_user()
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = user.create('/api/v2/manage/users', body)
        self.assertEqual(403, response.status_code)

    def test_get_user_should_return_200(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'/api/v2/manage/users/{identifier}')
        self.assertEqual(200, response.status_code)

    def test_get_user_should_return_user_email(self):
        user_email = 'new_user_email'
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': user_email,
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'/api/v2/manage/users/{identifier}').json()
        self.assertEqual(user_email, response['user_email'])

    def test_get_user_should_return_user_name(self):
        user_name = 'new_user'
        body = {
            'user_name': user_name,
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertEqual(user_name, response['user_name'])

    def test_get_user_should_return_user_login(self):
        user_login = 'new_user_login'
        body = {
            'user_name': 'new_user',
            'user_login': user_login,
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertEqual(user_login, response['user_login'])

    def test_get_user_should_return_user_is_service_account(self):
        user_is_service_account = True
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': user_is_service_account,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertEqual(user_is_service_account, response['user_is_service_account'])

    def test_get_user_should_return_404_when_user_not_found(self):
        response = self._subject.get(f'api/v2/manage/users/{_IDENTIFIER_FOR_NONEXISTENT_OBJECT}')
        self.assertEqual(404, response.status_code)

    def test_get_user_should_return_403_when_user_has_no_permission_to_get_user(self):
        user = self._subject.create_dummy_user()
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = user.get(f'api/v2/manage/users/{identifier}')
        self.assertEqual(403, response.status_code)

    def test_get_user_should_not_return_user_password(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertNotIn('user_password', response)

    def test_get_user_should_return_user_active_equal_false(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
            'user_active': False,
        }
        response = self._subject.create('api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertFalse(response['user_active'])

    def test_get_user_should_return_user_api_key(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.get(f'api/v2/manage/users/{identifier}').json()
        self.assertIn('user_api_key', response)

    def test_update_user_should_return_200(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.update(f'/api/v2/manage/users/{identifier}', body)
        self.assertEqual(200, response.status_code)

    def test_update_user_should_update_field_user_name(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        user_name = 'new_user'
        body = {
            'user_name': user_name,
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.update(f'/api/v2/manage/users/{identifier}', body).json()
        self.assertEqual(user_name, response['user_name'])

    def test_update_user_should_return_200_when_field_is_user_name_changed(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        body = {
            'user_name': 'new_user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.update(f'/api/v2/manage/users/{identifier}', body)
        self.assertEqual(200, response.status_code)

    def test_update_user_should_return_403_when_user_has_no_permission_to_update_user(self):
        user = self._subject.create_dummy_user()
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'NEW_user_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        body = {
            'user_name': 'new_user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = user.update(f'api/v2/manage/users/{identifier}', body)
        self.assertEqual(403, response.status_code)

    def test_update_user_should_return_404_when_user_not_found(self):
        body = {
            'user_name': 'new_user',
            'user_login': 'new_user_login',
            'user_email': 'new_user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.update(f'api/v2/manage/users/{_IDENTIFIER_FOR_NONEXISTENT_OBJECT}', body)
        self.assertEqual(404, response.status_code)

    def test_update_user_when_body_is_empty_should_return_200(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.update(f'/api/v2/manage/users/{identifier}', {})
        self.assertEqual(200, response.status_code)

    def test_delete_user_should_return_204(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
            'user_active': False
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = self._subject.delete(f'/api/v2/manage/users/{identifier}')
        self.assertEqual(204, response.status_code)

    def test_get_user_should_return_404_after_delete_user(self):
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
            'user_active': False
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        self._subject.delete(f'/api/v2/manage/users/{identifier}')
        response = self._subject.get(f'api/v2/manage/users/{identifier}')
        self.assertEqual(404, response.status_code)

    def test_delete_user_should_return_403_when_user_is_denied_permission_to_access_user(self):
        user = self._subject.create_dummy_user()
        body = {
            'user_name': 'user',
            'user_login': 'user_login',
            'user_email': 'user_email',
            'user_password': 'User_password_17_@',
            'user_is_service_account': True,
            'user_isadmin': True,
        }
        response = self._subject.create('/api/v2/manage/users', body).json()
        identifier = response['user_id']
        response = user.delete(f'/api/v2/manage/users/{identifier}')
        self.assertEqual(403, response.status_code)

    def test_delete_user_should_return_404_when_user_not_found(self):
        response = self._subject.delete(f'/api/v2/manage/users/{_IDENTIFIER_FOR_NONEXISTENT_OBJECT}')
        self.assertEqual(404, response.status_code)

    def test_delete_user_should_return_400_when_user_is_active(self):
        response = self._subject.delete(f'/api/v2/manage/users/{ADMINISTRATOR_USER_IDENTIFIER}')
        self.assertEqual(400, response.status_code)

    def test_delete_user_should_return_204_when_it_has_access_to_a_customer(self):
        identifier = self._subject.create_dummy_user().get_identifier()
        self._subject.update(f'/api/v2/manage/users/{identifier}', {'user_active': False})
        customer_identifier = self._subject.create_dummy_customer()
        body = {'customers_membership': [customer_identifier]}
        self._subject.create(f'/manage/users/{identifier}/customers/update', body)

        response = self._subject.delete(f'/api/v2/manage/users/{identifier}')
        self.assertEqual(204, response.status_code)

    def test_delete_user_should_return_400_when_there_is_assets_comment_by_the_user(self):
        case_identifier = self._subject.create_dummy_case()
        body = {'asset_type_id': 1, 'asset_name': 'admin_laptop_test'}
        response = self._subject.create(f'/api/v2/cases/{case_identifier}/assets', body).json()
        object_identifier = response['asset_id']

        user = self._subject.create_dummy_user()
        user_identifier = user.get_identifier()
        body = {
            'access_level': IRIS_CASE_ACCESS_LEVEL_FULL_ACCESS,
            'cases_list': [case_identifier]
        }
        self._subject.create(f'/manage/users/{user_identifier}/cases-access/update', body)

        user.create(f'/api/v2/assets/{object_identifier}/comments', {})

        self._subject.update(f'/api/v2/manage/users/{user.get_identifier()}', {'user_active': False})
        response = self._subject.delete(f'/api/v2/manage/users/{user.get_identifier()}')
        self.assertEqual(400, response.status_code)

    def test_delete_user_should_return_400_when_there_is_alerts_comment_by_the_user(self):
        user = self._subject.create_dummy_user([IRIS_PERMISSION_SERVER_ADMINISTRATOR, IRIS_PERMISSION_ALERTS_WRITE])

        body = {
            'alert_title': 'title',
            'alert_severity_id': 4,
            'alert_status_id': 3,
            'alert_customer_id': 1,
        }
        response = user.create('/api/v2/alerts', body).json()
        object_identifier = response['alert_id']
        user.create(f'/api/v2/alerts/{object_identifier}/comments', {})
        self._subject.update(f'/api/v2/manage/users/{user.get_identifier()}', {'user_active': False})
        response = self._subject.delete(f'/api/v2/manage/users/{user.get_identifier()}')
        self.assertEqual(400, response.status_code)
