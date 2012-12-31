"""
Implementation main.py for the TracTicketLimitPlugin.

Copyright (c) 2012, Missing Pixel Studios, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this software except in compliance with the License.  You
may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.
"""
from trac.core import *
from trac.ticket.api import ITicketManipulator
import trac.ticket.query as query
from trac.config import ListOption, BoolOption, Option
from trac.util.datefmt import (
    datetime, format_datetime, from_utimestamp, to_utimestamp, utc
)
from pytz import timezone

class ListPairOption(ListOption):
    """Descriptor for configuration options that contain multiple values
    in pairs separated by specific characters.

    ExampleOption = Dogs:6, Cats:8, Free Range Chickens:12
    """

    def __init__(self, section, name, default=None, itemsep=',', subsep=':', keep_empty=False,
                 doc='', doc_domain='tracini'):
        ListOption.__init__(self, section, name, default, itemsep, keep_empty, doc, doc_domain)
        self.subsep = subsep

    def accessor(self, section, name, default):
        pairs = {}
        for x in section.getlist(name, default, self.sep, self.keep_empty):
            k,v = x.split(self.subsep)
            pairs[k] = v
        return pairs

class LimitedTickets(Component):
    """Limits the number of tickets that can be created by a reporter per day
    for specified components
    """
    implements(ITicketManipulator)

    limited_components = ListPairOption('limited_tickets', 'component_limits')
    timezone_basis = Option('limited_tickets', 'timezone', default='UTC')
    admin_unlimited = BoolOption('limited_tickets', 'admin_unlimited', default='true')

    def prepare_ticket(self, req, ticket, fields, actions):
        pass

    def validate_ticket(self, req, ticket):
        today = datetime.now().date()
        day_start = datetime(today.year, today.month, today.day, 0, 0 ,0 ,0, timezone(self.timezone_basis))

        self.log.debug("LimitedTickets validate_ticket (ticket time: %s), restricted components: %s  %s, %u", ticket['time'], self.limited_components, day_start, to_utimestamp(day_start))
        if not 'TICKET_ADMIN' in req.perm or not self.admin_unlimited:
            # is new ticket for a limited component
            if not ticket.exists and ticket['component'] in self.limited_components:
                component = ticket['component']
                reporter = ticket['reporter']
                perday = self.limited_components[component]
                # check that the ticket doesn't violate the limit
                rows = self.env.db_query("SELECT count(id) FROM ticket WHERE reporter=%s"
                                        "and component=%s and time>%s",
                                        (reporter, component, to_utimestamp(day_start)))
                self.log.debug("Ticket Creation Attempt with restricted component: %s, rows: %s", component, rows)
                if rows and int(rows[0][0]) >= int(perday):
                    return [(None, "Only %u ticket(s)/day allowed for %s" % (int(perday),component))]
        return []

