import attr
from ndk.construct import Construct
from ndk.directives import *


@attr.s
class ContactGroupDirective(Construct):
    __object_type__ = 'contactgroup'

    contactgroup_name = PrimaryKey()
    alias = StringField(required=True)
    members = OneToMany('Contact')
    contactgroup_members = OneToMany('ContactGroup')

    @property
    def pk(self):
        return self.contactgroup_name
