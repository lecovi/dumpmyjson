"""
    dumpmyjson.main.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Main models module.

    :copyright: (c) 2017 by Cooperativa de Trabajo BITSON Ltda..
    :author: Leandro E. Colombo Viña (i5) <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
from copy import deepcopy
# Third-party imports
from sqlalchemy.dialects.postgresql import JSON
# BITSON imports
from app.extensions import db, AppModel


class JSONData(AppModel):
    __tablename__ = 'data'

    description = None
    erased = None
    data = db.Column(JSON)

    methods = ['GET', 'POST']

    # We copy `preprocessors` and `postprocessors` dicts and `include_methods`
    # list from AppModel because otherwise dict are shared between classes.
    preprocessors = AppModel.preprocessors.copy()
    postprocessors = AppModel.postprocessors.copy()
    include_methods = AppModel.include_methods.copy()
    # The model can `exclude_columns` OR `include_columns`, not BOTH.
    # exclude_columns = list()
    # include_columns = list()
    validation_exceptions = AppModel.validation_exceptions.copy()

    preprocessors['POST'] = deepcopy(AppModel.preprocessors['POST'])
    preprocessors['GET_SINGLE'] = deepcopy(AppModel.preprocessors['GET_SINGLE'])
    preprocessors['GET_MANY'] = deepcopy(AppModel.preprocessors['GET_MANY'])

    postprocessors['POST'] = deepcopy(AppModel.postprocessors['POST'])
    postprocessors['GET_SINGLE'] = deepcopy(AppModel.postprocessors[
                                                'GET_SINGLE'])
    postprocessors['GET_MANY'] = deepcopy(AppModel.postprocessors['GET_MANY'])


    # preprocessors['POST'].append(logged_user)
    # preprocessors['GET_SINGLE'].append(logged_user)
    # preprocessors['GET_MANY'].append(logged_user)
