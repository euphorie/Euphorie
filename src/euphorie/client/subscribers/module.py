from euphorie.client.model import SurveyTreeItem
from sqlalchemy import and_
from sqlalchemy import Integer
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast
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

    # First, set all paths and zodb_paths to bogus values (extra zeros)
    # to avoid constraint errors
    for risk in custom_risks:
        risk.path = risk.path + "000"
        risk.zodb_path = risk.zodb_path + "000"

    ordered_custom_risks = (
        session.query(SurveyTreeItem)
        .filter(
            and_(
                SurveyTreeItem.session_id == context.session_id,
                SurveyTreeItem.path.like(context.path + "%"),
                SurveyTreeItem.type == "risk",
            )
        )
        .order_by(cast(func.split_part(SurveyTreeItem.zodb_path, "/", 2), Integer))
    )

    # Iterate over the risks in their natural order. Close any gaps in numbering
    for count, risk in enumerate(ordered_custom_risks):
        risk.zodb_path = f"custom-risks/{count + 1}"

    # Now, set the path according to the zodb_path (= natural order)
    for risk in custom_risks:
        risk.path = "%s%03d" % (context.path, int(risk.zodb_path.split("/")[-1]))
