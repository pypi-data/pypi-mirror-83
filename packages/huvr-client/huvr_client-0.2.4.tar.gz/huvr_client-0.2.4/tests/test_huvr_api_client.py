#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `huvr_api_client` package."""


import unittest
import sys
import os

# look for libraries that are configured by './build.sh'
cwd = os.getcwd()

# Add `/lib` to the path to pick up our pip installed 3rd party requirements
sys.path[0:0] = ["{}/lib".format(cwd)]

# Add '/huvr_api_client' to the path to make this runnable out of the source tree
sys.path[0:0] = ["{}/huvr_api_client".format(cwd)]

from huvr_api_client import Client


class TestHuvr_api_client(unittest.TestCase):
    """Tests for `huvr_api_client` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        subdomain = "jeffield"
        running_in = "testing"  # developer, testing, staging, production

        # subdomain = "jeffield2"
        # running_in = "developer"  # developer, testing, staging, production

        # Set up HUVRClient
        self.client = Client(subdomain=subdomain, running_in=running_in, verbose=True)
        # self.client.login(username='unittest@example.com', password='unittest')
        self.client.login()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    #  .--------------------------.
    # |  Infrastructure Testing    |
    # |  GET Response 200 testing  |
    #  '--------------------------'
    def test_response_profiles(self):
        """ Resonse code of the profile request.
            GET /api/profiles """
        (res_code, profiles) = self.client.profiles()
        self.assertEqual(res_code, 200)

    def test_response_checklists(self):
        """ GET /api/checklists """
        (res_code, checklists) = self.client.checklists()
        self.assertEqual(res_code, 200)

    def test_response_specific_checklist(self):
        """ GET /api/checklists/<checklist_id> """
        (res_code, checklists) = self.client.checklists()
        last_checklist_id = None
        if res_code == 200:
            for checklist in checklists['results']:
                last_checklist_id = checklist['id']

            (res_code_one_checklist, checklist) = self.client.checklists(last_checklist_id)
            self.assertEqual(res_code_one_checklist, 200)

    def test_response_checklist_v2_json(self):
        """ GET /api/v2/checklists/<checklist_id>"""
        (res_code, checklists) = self.client.checklists()
        # print json.dumps(checklists, indent=4)
        last_checklist_id = None
        if res_code == 200:
            for checklist in checklists['results']:
                last_checklist_id = checklist['id']

            (res_code_one_checklist, checklist) = self.client.checklist_v2(last_checklist_id)
            self.assertEqual(res_code_one_checklist, 200)

    def test_response_checklist_v2_csv(self):
        """ GET /api/v2/checklists/<checklist_id>"""
        (res_code, checklists) = self.client.checklists()
        # print json.dumps(checklists, indent=4)
        last_checklist_id = None
        if res_code == 200:
            for checklist in checklists['results']:
                last_checklist_id = checklist['id']

            (res_code_one_checklist, checklist) = self.client.checklist_v2(last_checklist_id, download_csv=True)
            self.assertEqual(res_code_one_checklist, 200)

    def test_response_project_types(self):
        """ GET /api/project_types """
        (res_code, project_types) = self.client.project_types()
        self.assertEqual(res_code, 200)

    def test_response_project_type(self):
        """ GET /api/project_types """
        (res_code, project_types) = self.client.project_types()
        if res_code == 200:
            for project_type in project_types['results']:
                (res_code_pt, project_type) = self.client.project_types(project_type['id'])
                self.assertEqual(res_code_pt, 200)
                break

    def test_response_project_name_lookup(self):
        """ GET /api/project_types """
        (res_code, project_types) = self.client.project_types()
        if res_code == 200:
            for project_type in project_types['results']:
                (res_code_pt, project_type) = self.client.project_type_name_lookup(project_type['name'])
                self.assertEqual(res_code_pt, 200)
                # import json; print json.dumps(project_type, indent=4)
                break

    # def test_response_project_type_defects_json(self):
    #     """ OBE: GET /api/project_type/<project_type_id>/defects """
    #     (res_code, project_types) = self.client.project_types()
    #     if res_code == 200:
    #         for project_type in project_types['results']:
    #             (res_code_pt, projects_defects) = self.client.project_type_defects(project_type['id'])
    #             self.assertEqual(res_code_pt, 200)
    #             break

    # def test_response_project_type_defects_csv(self):
    #     """ OBE: GET /api/project_type/<project_type_id>/defects?download_csv=True """
    #     (res_code, project_types) = self.client.project_types()
    #     if res_code == 200:
    #         for project_type in project_types['results']:
    #             (res_code_pt, projects_defects) = self.client.project_type_defects(project_type['id'], download_csv=True)
    #             self.assertEqual(res_code_pt, 200)
    #             break

    # def test_response_project_type_projects_json(self):
    #     """ GET /api/project_types """
    #     (res_code, project_types) = self.client.project_types()
    #     if res_code == 200:
    #         for project_type in project_types['results']:
    #             (res_code_pt, projects_meta) = self.client.project_type_projects_metadata(project_type['id'])
    #             self.assertEqual(res_code_pt, 200)
    #             break

    # def test_response_project_type_projects_csv(self):
    #     """ GET /api/project_types """
    #     (res_code, project_types) = self.client.project_types()
    #     if res_code == 200:
    #         for project_type in project_types['results']:
    #             (res_code_pt, projects_meta) = self.client.project_type_projects_metadata(project_type['id'], download_csv=True)
    #             self.assertEqual(res_code_pt, 200)
    #             break

    def test_response_project_type_project_ids(self):
        """ GET /api/project_type/<project_type_id>/projects_ids """
        (res_code, project_types) = self.client.project_types()
        if res_code == 200:
            for project_type in project_types['results']:
                (res_code_pt, project_ids) = self.client.project_type_project_ids(project_type['id'])
                # import json; print(json.dumps(project_ids, indent=4))
                self.assertEqual(res_code_pt, 200)
                break

    def test_response_project_type_project_defects_json(self):
        """ GET /api/projects/<project_id>/defects """
        (res_code, project_types) = self.client.project_types()
        if res_code == 200:
            found_project_defects = False
            for project_type in project_types['results']:
                if not found_project_defects:
                    (res_code_pt, project_ids) = self.client.project_type_project_ids(project_type['id'])
                    for project_id in project_ids:
                        (res_code_pd, project_defects) = self.client.project_defects(project_id)
                        # import json; print(json.dumps(project_defects, indent=4))
                        self.assertEqual(res_code_pd, 200)
                        found_project_defects = True
                        break

    def test_response_project_type_project_defects_csv(self):
        """ GET /api/projects/<project_id>/defects?download_csv=True """
        (res_code, project_types) = self.client.project_types()
        if res_code == 200:
            found_project_defects = False
            for project_type in project_types['results']:
                if not found_project_defects:
                    (res_code_pt, project_ids) = self.client.project_type_project_ids(project_type['id'])
                    for project_id in project_ids:
                        (res_code_pd, project_defects) = self.client.project_defects(project_id, download_csv=True)
                        self.assertEqual(res_code_pd, 200)
                        found_project_defects = True
                        break

    def test_response_projects_meta_cursor(self):
        """ GET /api/projects_meta?offset=<cursor> """
        (res_code, projects) = self.client.projects_meta(cursor_query=True)
        self.assertEqual(res_code, 200)

    def test_response_project_meta(self):
        """ GET /api/projects_meta/<project_id> """
        (res_code, projects) = self.client.projects_meta(cursor_query=False)
        # import json
        # print(json.dumps(projects, indent=4))
        self.assertEqual(res_code, 200)

    # def test_response_project_types(self):
    #     """ GET /api/project_types """
    #     (res_code, project_types) = client.project_types()
    #     self.assertEqual(res_code, 200)

    #     checklist_id = None
    #     (res_code, project_types) = client.project_types()
    #     if res_code == 200:
    #         found_projects = False
    #         for project_type in project_types['results']:
    #             if not found_projects:
    #                 project_type_id = project_type['id']
    #                 (res_code, projects) = client.project_type_projects_metadata(project_type_id)
    #                 if res_code == 200:
    #                     if projects:
    #                         found_projects = True
    #                         for project in projects['projects']:
    #                             checklist_id = project['checklist_id']
    #                             if checklist_id:
    #                                 break
    #                 else:
    #                     print("{} {}".format(res_code, projects))
    #     else:
    #         print("{} {}".format(res_code, project_types))

    #  .--------------------------.
    # |  Infrastructure Testing    |
    # |  GET Data testing          |
    #  '--------------------------'

# checklist_v2
