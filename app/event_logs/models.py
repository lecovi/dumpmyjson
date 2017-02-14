"""
    dumpmyjson.models
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by Cooperativa de Trabajo BITSON Ltda..
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
import json
from copy import deepcopy
from datetime import datetime
# Third-party imports
from flask_restless import ProcessingException
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import IntegrityError
# BITSON imports
from app.extensions import db, AppModel
from app.logger import console_logger


class ActionGroup(AppModel):
    __tablename__ = 'action_groups'

    methods = ['GET']
    # We copy `preprocessors` and `postprocessors` dicts and `include_methods`
    # list from AppModel because otherwise dict are shared between classes.
    preprocessors = AppModel.preprocessors.copy()
    postprocessors = AppModel.postprocessors.copy()
    include_methods = AppModel.include_methods.copy()
    # The model can `exclude_columns` OR `include_columns`, not BOTH.
    # exclude_columns = list()
    # include_columns = list()
    validation_exceptions = AppModel.validation_exceptions.copy()

    preprocessors['GET_SINGLE'] = deepcopy(AppModel.preprocessors['GET_SINGLE'])
    preprocessors['GET_MANY'] = deepcopy(AppModel.preprocessors['GET_MANY'])
    postprocessors['GET_SINGLE'] = deepcopy(AppModel.postprocessors[
                                                'GET_SINGLE'])
    postprocessors['GET_MANY'] = deepcopy(AppModel.postprocessors['GET_MANY'])


class Action(AppModel):
    __tablename__ = 'actions'

    action_group_id = db.Column(db.Integer,
                                db.ForeignKey('action_groups.id'), default=0)

    action_group = db.relationship('ActionGroup')

    methods = ['GET']
    # We copy `preprocessors` and `postprocessors` dicts and `include_methods`
    # list from AppModel because otherwise dict are shared between classes.
    preprocessors = AppModel.preprocessors.copy()
    postprocessors = AppModel.postprocessors.copy()
    include_methods = AppModel.include_methods.copy()
    # The model can `exclude_columns` OR `include_columns`, not BOTH.
    exclude_columns = ['action_group_id', ]
    # include_columns = list()
    validation_exceptions = AppModel.validation_exceptions.copy()

    preprocessors['GET_SINGLE'] = deepcopy(AppModel.preprocessors['GET_SINGLE'])
    preprocessors['GET_MANY'] = deepcopy(AppModel.preprocessors['GET_MANY'])
    postprocessors['GET_SINGLE'] = deepcopy(AppModel.postprocessors[
                                                'GET_SINGLE'])
    postprocessors['GET_MANY'] = deepcopy(AppModel.postprocessors['GET_MANY'])


class EventLog(db.Model):
    __tablename__ = 'event_logs'

    HTTP_METHODS = {
        'POST': 1,
        'GET': 2,
        'PUT': 3,
        'DELETE': 4,
    }

    id = db.Column(db.Integer, primary_key=True, index=True)
    url = db.Column(db.String(), nullable=False, index=True)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    params = db.Column(JSON)
    response = db.Column(JSON)
    code_version = db.Column(db.String(15), nullable=False, index=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # user = db.relationship('User')
    action = db.relationship('Action')

    @classmethod
    def register_http(cls, method, response, **kwargs):
        action_id = cls.HTTP_METHODS[method]
        rd = {
            'status': {
                'code': response.status_code,
                'description': response.status,
            },
            'headers': dict((k, v) for k, v in response.headers.to_list()),
            'values': json.loads(response.get_data('utf-8')),
        }
        event = cls(action_id=action_id, response=rd, **kwargs)

        db.session.add(event)
        db.session.commit()

    @staticmethod
    def idempotent_insert(item_list):
        for item in item_list:
            try:
                db.session.add(item)
                db.session.commit()
            except IntegrityError as e:
                console_logger.warn(
                    "\033[33mWARNING: {}Skipping...\n\033[0m".format(
                        e.orig.args[0])
                )
                db.session.rollback()
                continue

    methods = ['GET']

    validators = []

    results_per_page = 15
    max_results_per_page = 50

    preprocessors = dict(
        POST=list(),
        GET_SINGLE=list(),
        GET_MANY=list(),
        PATCH_SINGLE=list(),
        PATCH_MANY=list(),
        DELETE_SINGLE=list(),
        DELETE_MANY=list(),
    )
    postprocessors = dict(
        POST=list(),
        GET_SINGLE=list(),
        GET_MANY=list(),
        PATCH_SINGLE=list(),
        PATCH_MANY=list(),
        DELETE_SINGLE=list(),
        DELETE_MANY=list(),
    )
    include_methods = list()
    exclude_columns = list()
    include_columns = None
    validation_exceptions = [ProcessingException, ]
