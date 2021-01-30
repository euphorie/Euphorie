# coding=utf-8
from euphorie.client.model import SurveyTreeItem
from sqlalchemy import and_
from sqlalchemy.sql import func
from z3c.saconfig import Session


def handle_custom_risks_order(context, event):
    session = Session()

    custom_risks = session.query(SurveyTreeItem).filter(
        and_(
            SurveyTreeItem.session_id == context.session_id,
            SurveyTreeItem.path.like(context.path + "%"),
            SurveyTreeItem.type == "risk",
        )
    )

    # First, set all zodb_paths to bogus "XXX" values, to avoid constraint errors
    custom_risks.update(
        {
            SurveyTreeItem.path: context.path
            + func.lpad(func.split_part(SurveyTreeItem.zodb_path, "/", 2), 3, "0")
            + "xxx"
        },
        synchronize_session=False,
    )

    # Now, set the zodb_path according to the path (= natural order)
    custom_risks.update(
        {
            SurveyTreeItem.path: context.path
            + func.lpad(func.split_part(SurveyTreeItem.zodb_path, "/", 2), 3, "0")
        },
        synchronize_session=False,
    )
