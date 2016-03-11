# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.records import RecordsControlPanel
from plone.app.registry.testing import PLONE_APP_REGISTRY_INTEGRATION_TESTING

import types
import unittest2 as unittest


class TestRegistryBaseControlpanel(unittest.TestCase):

    layer = PLONE_APP_REGISTRY_INTEGRATION_TESTING

    def test_registry_base_controlpanel__control_panel_url(self):
        """Test, if control_panel_url property of the base controlpanel returns
        the correct url.
        """
        view = ControlPanelFormWrapper(None, None)
        self.assertEqual(
            view.control_panel_url,
            u'http://nohost/plone/@@overview-controlpanel'
        )


class TestRecordsControlPanel(unittest.TestCase):

    layer = PLONE_APP_REGISTRY_INTEGRATION_TESTING

    def test_records_control_panel__control_panel_url(self):
        """Test, if control_panel_url property of the registry controlpanel
        returns the correct url.
        """
        view = RecordsControlPanel(None, None)
        self.assertEqual(
            view.control_panel_url,
            u'http://nohost/plone/@@overview-controlpanel'
        )
