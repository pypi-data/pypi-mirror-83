import os
from unittest import TestCase
from unittest.mock import patch, call, Mock

from ipaconnector.connector import IpaConnector
from ipaconnector.jdbc import Hive


class TestCaseSeven(TestCase):
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
    def test_case_seven(self, getpass, socket, ssh, shell, cluster, jdbc):
        getpass.getuser.return_value = "runuser"
        self.hive_mock = Hive(jdbc)
        cluster.get_hive_interface.return_value = self.hive_mock
        cluster.HOST = "elara-edgeg-u1-n01"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ut.run(os.path.join(os.path.dirname(__file__), 'sample_seven.json'))
