import os
import unittest
from vortex.rules import mapper
from . import mock_galaxy


class TestResourceParserRole(unittest.TestCase):

    @staticmethod
    def _map_to_destination(tool, user):
        galaxy_app = mock_galaxy.App()
        job = mock_galaxy.Job()
        mapper_config = os.path.join(os.path.dirname(__file__), 'fixtures/mapping-role.yml')
        mapper.ACTIVE_DESTINATION_MAPPER = None
        return mapper.map_tool_to_destination(galaxy_app, job, tool, user, mapper_config_file=mapper_config)

    def test_map_default_role(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('ford', 'prefect@vortex.org')

        destination = self._map_to_destination(tool, user)
        self.assertEqual(destination.id, "k8s_environment")

    def test_map_overridden_role(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('gargravarr', 'fairycake@vortex.org', roles=["training"])

        destination = self._map_to_destination(tool, user)
        self.assertIsNone(destination)

    def test_map_role_by_regex(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('gargravarr', 'fairycake@vortex.org', roles=["newtraining2021group"])

        destination = self._map_to_destination(tool, user)
        self.assertEqual(destination.id, "k8s_environment")