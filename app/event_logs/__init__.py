"""
    dumpmyjson.__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by Cooperativa de Trabajo BITSON Ltda..
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
# BITSON imports


def init_event_logs():
    from .models import ActionGroup, Action, EventLog

    action_groups = [
        ActionGroup(id=0, description='N/A'),
        ActionGroup(description='HTTP methods'),
    ]

    ActionGroup.idempotent_insert(action_groups)

    actions = [
        Action(id=0, description='N/A', action_group_id=0),
        Action(description='Create', action_group_id=1),
        Action(description='Read', action_group_id=1),
        Action(description='Update', action_group_id=1),
        Action(description='Delete', action_group_id=1),
    ]

    Action.idempotent_insert(actions)

    event_logs = [
        EventLog(id=0, url='N/A', action_id=0, code_version='0.0.0'),
    ]

    EventLog.idempotent_insert(event_logs)


def init_demo_event_logs():
    pass
