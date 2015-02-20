# Copyright 2014 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from cloudinstall.charms import CharmBase

log = logging.getLogger('cloudinstall.charms.cinder')


class CharmCinder(CharmBase):

    """ Cinder directives """

    charm_name = 'cinder'
    charm_rev = 10
    display_name = 'Cinder'
    related = {'glance': ('cinder:image-service', 'glance:image-service'),
               'rabbitmq-server': ('rabbitmq-server:amqp',
                                   'cinder:amqp'),
               'keystone': ('cinder:identity-service',
                            'keystone:identity-service'),
               'nova-cloud-controller': (
                   'nova-cloud-controller:cinder-volume-service',
                   'cinder:cinder-volume-service')}
    deploy_priority = 5
    disabled = False

    def set_relations(self):
        if not self.wait_for_agent([self.charm_name,
                                    'glance',
                                    'keystone',
                                    'rabbitmq-server',
                                    'nova-cloud-controller']):
            return True
        for charm in self.related.keys():
            try:
                rv = self.juju.add_relation(self.related[charm])
                log.debug("add_relation {} "
                          "returned {}".format(charm, rv))
            except:
                log.exception("{} not ready for relation".format(charm))
                return True

__charm_class__ = CharmCinder
