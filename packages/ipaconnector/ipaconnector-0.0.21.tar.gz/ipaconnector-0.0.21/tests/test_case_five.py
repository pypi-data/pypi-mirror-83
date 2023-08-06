import os
from unittest import TestCase
from unittest.mock import patch, call

from ipaconnector.connector import IpaConnector


class TestFunctional(TestCase):
    def setUp(self):
        self.sample = os.path.join(os.path.dirname(__file__), 'sample.json')
        with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
            self.ut = IpaConnector('ipa.server.net')
            self._client_mock = self._Client_mock()
            self.ut.connect(kerberos=True)

    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def test_case_sample_two(self, getpass, socket, ssh, shell):
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ut.run(os.path.join(os.path.dirname(__file__), 'sample_five.json'))
        self._client_mock.user_add.assert_not_called()
        self._client_mock.user_del.assert_not_called()
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_del.assert_not_called()
        self._client_mock.group_add_member.assert_called_once_with(a_cn='dsi_datas_bigdata_preprod',
                                                                   o_user='chhenner')

        self._client_mock.group_remove_member.assert_called_once_with(a_cn='dsi_moe_dev_bigdata',
                                                                      o_user='chhenner')
