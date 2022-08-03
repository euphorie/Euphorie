from base64 import encodebytes
from datetime import date
from datetime import datetime
from euphorie.client.model import ActionPlan
from euphorie.client.model import BaseObject
from euphorie.client.model import Company
from euphorie.client.model import Risk
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.client.model import SurveyTreeItem
from euphorie.client.model import Training
from sqlalchemy.orm.query import Query
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


class ISA2DictAdapter(Interface):
    def get_children():
        """Return a dictionary containing
        whatever you like to be defined as children of this table
        """

    def __call__():
        """Return a dictionary representation of this object"""


@implementer(ISA2DictAdapter)
@adapter(BaseObject)
class SA2DictAdapter:
    def __init__(self, context):
        self.context = context

    def get_children(self):
        return {}

    def __call__(self):
        table = self.context.__table__
        data = {}
        for column in table.columns:
            try:
                data[column.key] = getattr(self.context, column.key)
            except AttributeError:
                # Happens when using polymorphic tables:
                # the object might no have all the attributes set
                pass

        return {
            "table": table.name,
            "data": data,
            "children": self.get_children(),
        }


@adapter(Risk)
class Risk2DictAdapter(SA2DictAdapter):
    def get_children(self):
        return {
            ActionPlan.__table__.name: Session.query(ActionPlan).filter(
                ActionPlan.risk_id == self.context.id
            )
        }


@adapter(SurveySession)
class SurveySession2DictAdapter(SA2DictAdapter):
    def get_children(self):
        return {
            klass.__table__.name: Session.query(klass).filter(
                klass.session_id == self.context.id
            )
            for klass in [Company, SurveyTreeItem, Training]
        }


class SAJsonEncoder(json.JSONEncoder):

    __children_mapping__ = {
        "session": [Company, SurveyTreeItem, Training],
        "risk": [ActionPlan],
    }

    def default(self, obj):
        if isinstance(obj, BaseObject):
            adapter = ISA2DictAdapter(obj)
            return adapter()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Query):
            return obj.all()
        elif isinstance(obj, bytes):
            return encodebytes(obj).decode("ascii")
        return super().default(obj)
