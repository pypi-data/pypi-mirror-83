import os
from unittest import TestCase
from unittest.mock import patch, call, Mock

from ipaconnector.connector import IpaConnector
from ipaconnector.jdbc import Hive


class TestCaseSix(TestCase):
    def setUp(self):
        self.sample = os.path.join(os.path.dirname(__file__), 'sample.json')
        with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
            self.ut = IpaConnector('ipa.server.net')
            self._client_mock = self._Client_mock()
            self.ut.connect(kerberos=True)

    @patch("ipaconnector.jdbc.jaydebeapi")
    @patch("ipaconnector.connector.CALLISTO")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def test_case_sample_two(self, getpass, socket, ssh, shell, cluster, jdbc):
        getpass.getuser.return_value = "runuser"
        self.hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = self.hive_mock
        cluster.HOST = "elara-edgeg-u1-n01"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ut.run(os.path.join(os.path.dirname(__file__), 'sample_six.json'))
        self.hive_mock.revoke_role_from_group.assert_has_calls([
            call(group='dssuser', role='user_access_rw_ble_zi00_adm'),
            call(group='dssuser', role='user_access_rw_ble_zi00_source'),
            call(group='dssuser', role='user_access_rw_ble_zi00_trv'),
            call(group='dssuser', role='user_access_rw_ble_zi00_socle'),
            call(group='dssuser', role='user_access_rw_ble_zi00_metier'),
            call(group='dssuser', role='user_access_rw_ble_zi00_extr'),
            call(group='dssuser', role='user_access_rw_prd_zi02_adm'),
            call(group='dssuser', role='user_access_rw_prd_zi02_source'),
            call(group='dsi_moe_dev_bigdata', role='user_access_r_prv_moa_zi29_usr'),
            call(group='dssuser', role='user_access_rw_prd_zi02_trv'),
            call(group='dssuser', role='user_access_rw_prd_zi02_socle'),
            call(group='dssuser', role='user_access_rw_prd_zi02_metier'),
            call(group='dssuser', role='user_access_rw_prd_zi02_extr'),
            call(group='dssuser', role='user_access_rw_prv_moa_zi29_usr'),
            call(group='dssuser', role='user_access_rw_prv_moe_zi03_usr')
        ], any_order=True)
        self.hive_mock.add_group_to_role.assert_has_calls([
            call(group='dsssysadm', role='user_access_rw_ble_zi00_adm'),
            call(group='dsssysadm', role='user_access_rw_ble_zi00_source'),
            call(group='dsssysadm', role='user_access_rw_ble_zi00_trv'),
            call(group='dsssysadm', role='user_access_rw_ble_zi00_socle'),
            call(group='dsssysadm', role='user_access_rw_ble_zi00_metier'),
            call(group='dsssysadm', role='user_access_rw_ble_zi00_extr'),
            call(group='dsi_moe_bigdata_preprod', role='user_access_r_prv_moa_zi29_usr'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_adm'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_source'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_trv'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_socle'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_metier'),
            call(group='dsssysadm', role='user_access_rw_prd_zi02_extr'),
            call(group='dsssysadm', role='user_access_rw_prv_moa_zi29_usr'),
            call(group='dsssysadm', role='user_access_rw_prv_moe_zi03_usr')
        ], any_order=True)
