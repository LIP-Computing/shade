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
                    shared=False,
                    admin_state_up=True
                )
            )
        )

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    def test_create_network_specific_tenant(self, mock_neutron):
        self.cloud.create_network("netname", project_id="project_id_value")
        mock_neutron.create_network.assert_called_with(
            body=dict(
                network=dict(
                    name='netname',
                    shared=False,
                    admin_state_up=True,
                    tenant_id="project_id_value",
                )
            )
        )


    @mock.patch.object(shade.OpenStackCloud, 'get_network')
    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    def test_delete_network(self, mock_neutron, mock_get):
        mock_get.return_value = dict(id='net-id', name='test-net')
        self.assertTrue(self.cloud.delete_network('test-net'))
        mock_get.assert_called_once_with('test-net')
        mock_neutron.delete_network.assert_called_once_with(network='net-id')

