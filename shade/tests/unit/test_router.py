# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import testtools

import shade
from shade.tests.unit import base


class TestRouter(base.TestCase):

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    def test_create_router(self, mock_neutron):
        self.cloud.create_router("routername")
        mock_neutron.create_router.assert_called_with(
            body=dict(
                router=dict(
                    name='routername',
                    admin_state_up=True
                )
            )
        )

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    def test_create_router_specific_tenant(self, mock_neutron):
        self.cloud.create_router("routername", project_id="project_id_value")
        mock_neutron.create_router.assert_called_with(
            body=dict(
                router=dict(
                    name='routername',
                    admin_state_up=True,
                    tenant_id="project_id_value",
                )
            )
        )

    @mock.patch.object(shade.OpenStackCloud, 'get_router')
    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    def test_delete_router(self, mock_neutron, mock_get):
        mock_get.return_value = dict(id='router-id', name='test-router')
        self.assertTrue(self.cloud.delete_router('test-router'))
        mock_get.assert_called_once_with('test-router')
        mock_neutron.delete_router.assert_called_once_with(router='router-id')

