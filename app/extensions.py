# Standard Lib imports
from datetime import datetime, date, time, timedelta
# Third-party imports
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restless import ProcessingException
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
# BITSON imports
from app.logger import console_logger

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


class AppModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(100), nullable=False, index=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow,
                           nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow(),
                           nullable=False)
    erased = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        items = dict((col, getattr(self, col))
                     for col in self.__table__.columns.keys())
        row = "{}<{}>".format(self.__class__.__name__, items)
        return row

    def __str__(self):
        return "{} --> {}.id={}".format(self.__class__,
                                        self.__class__.__tablename__, self.id)

    def export_data(self, exclude=None):
        response = dict()
        for attr, value in self.__dict__.items():
            if attr.startswith('_'):
                continue
            if exclude and attr in exclude:
                continue
            if isinstance(value, (date, time, datetime)):
                value = value.isoformat()
            if isinstance(value, timedelta):
                value = value.total_seconds()
            response.update({attr: value})
        return response

    def set_erased(self, commit=True):
        self.erased = True
        if commit:
            db.session.commit()

    def set_not_erased(self, commit=True):
        self.erased = False
        if commit:
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

    @classmethod
    def get_by(cls, erased=False, **kwargs):
        return db.session.query(cls).filter_by(erased=erased, **kwargs).first()

    @classmethod
    def create_fake(cls, **kwargs):
        item = cls.__init__(cls, **kwargs)
        db.session.add(item)
        db.session.commit()
        return item

    @classmethod
    def remove_fake(cls, item):
        cls.set_sequence_value(value=item.id - 1)
        db.session.delete(item)
        db.session.commit()

    @classmethod
    def get_sequence_name(cls):
        return "".join([cls.__tablename__, '_id_seq'])

    @classmethod
    def set_sequence_value(cls, value):
        sequence_name = cls.get_sequence_name()
        query = "SELECT setval('{sequence_name}', {value})".format(
            sequence_name=sequence_name, value=value)
        db.session.execute(query)
        db.session.commit()

    @classmethod
    def get_max_id(cls, erased=False):
        return db.session.query(func.max(cls.id)).filter_by(
            erased=erased).first()[0]

    @classmethod
    def get_invalid_id(cls):
        return db.session.query(func.max(cls.id)).first()[0] + 1

    @classmethod
    def update_sequence(cls, new_sequence_value=1):
        sequence = Sequence("".join([cls.__tablename__, "_id_seq"]))
        current_sequence_value = db.session.execute(sequence)
        while current_sequence_value < new_sequence_value:
            current_sequence_value = db.session.execute(sequence)

    methods = ['GET', 'POST', 'PUT', 'PATCH']
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
    exclude_columns = None
    include_columns = None
    validation_exceptions = [ProcessingException]


@db.event.listens_for(AppModel, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_on = datetime.utcnow()
