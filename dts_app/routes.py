from flask import render_template, request, Response
from .app import app, db
from .models import Passage, Collection


def not_found_xml(response):
    return Response(
        response,
        status=404,
        mimetype="text/xml"
    )


@app.route("/document")
def document():
    collection = Collection.get_by_identifier(request.args.get("id"))

    if not collection:
        return not_found_xml(
            render_template("error.xml", code=404, title="Document not found",
                            message="This collection does not exist in our database.")
        )

    if collection.collection_type != "Resource":
        return not_found_xml(
            render_template("error.xml", code=404, title="Document not readable",
                            message="This collection is not readable")
        )

    if request.args.get("ref"):
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order == request.args.get("ref")
            )
        ).first()
        if not passages:
            return not_found_xml(
                render_template("error.xml", code=404, title="Passage not found", message="This passage was not found")
            )
        passages = [passages]
    elif request.args.get("start") and request.args.get("end"):
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order.between(request.args.get("start"), request.args.get("end"))
            )
        ).all()
        if not passages:
            return not_found_xml(
                render_template("error.xml", code=404, title="Passage not found", message="This passage range"
                                                                                          " was not found")
            )
    else:
        passages = collection.passages

    return Response(
        render_template(
            "tei.xml",
            collection=collection,
            passages=passages
        ),
        mimetype="text/xml"
    )
