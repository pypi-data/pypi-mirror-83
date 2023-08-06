import base64

import requests as rq

from freshdesk_api_client import (
    utils,
    resources
)

class FreshdeskClient:
    BASE_URL = 'https://{}.freshdesk.com/api'

    def __init__(self, company, api_key, api_version='v2'):
        self._session = rq.Session()
        self._company = company
        self._api_key = api_key
        self._api_version = api_version

        self._base_url = utils.urljoin(FreshdeskClient.BASE_URL.format(self._company), self._api_version)
        self._resources = {
            'tickets': resources.TicketsPool(
                utils.urljoin(self._base_url, 'tickets'), self._session),
            'ticket_fields ': resources.TicketFieldsPool(
                utils.urljoin(self._base_url, 'admin', 'ticket_fields'), self._session),
            'conversations': resources.ConversationsPool(
                utils.urljoin(self._base_url, 'conversations'), self._session),
            'contacts': resources.ContactsPool(
                utils.urljoin(self._base_url, 'contacts'), self._session),
            'agents': resources.AgentsPool(
                utils.urljoin(self._base_url, 'agents'), self._session),
            'skills': resources.SkillsPool(
                utils.urljoin(self._base_url, 'skills'), self._session),
            'roles': resources.RolesPool(
                utils.urljoin(self._base_url, 'roles'), self._session),
            'groups': resources.GroupsPool(
                utils.urljoin(self._base_url, 'groups'), self._session),
            'companies': resources.CompaniesPool(
                utils.urljoin(self._base_url, 'companies'), self._session),
            'search': resources.SearchPool(
                utils.urljoin(self._base_url, 'search'), self._session),
        }

        self._authenticate()

    def _authenticate(self):
        basic_auth = '{}:X'.format(self._api_key).encode('utf-8')
        basic_auth = base64.b64encode(basic_auth).decode()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(basic_auth)
        }
        self._session.headers = headers

    @property
    def resources(self):
        """Return all resources as a list of Resources"""
        return self._resources

    @property
    def tickets(self):
        return self.resources.get('tickets')

    @property
    def conversations(self):
        return self.resources.get('conversations')

    @property
    def contacts(self):
        return self.resources.get('contacts')

    @property
    def agents(self):
        return self.resources.get('agents')

    @property
    def skills(self):
        return self.resources.get('skills')

    @property
    def roles(self):
        return self.resources.get('roles')

    @property
    def groups(self):
        return self.resources.get('groups')

    @property
    def companies(self):
        return self.resources.get('companies')

    @property
    def ticket_fields(self):
        return self.resources.get('ticket_fields')
