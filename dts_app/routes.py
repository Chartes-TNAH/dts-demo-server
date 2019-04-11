from flask import render_template, request, Response, url_for, jsonify
from .app import app, db
from .models import Passage, Collection


def not_found_xml(response):
    return Response(
        response,
        status=404,
        mimetype="text/xml"
    )


def json_error(title, message, code=404):
    j = jsonify({
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@type": "Status",
      "statusCode": code,
      "title": title,
      "description": message,
    })
    return j, code


def grouper(n, iterable):
    """ Group a sequence (iterable) into a sequence of n

    :param n: Grouping size
    :param iterable: List of identifiers
    :yield: List of list of size N
    """
    for pos in range(0, len(iterable), n):
        yield iterable[pos:pos + n]


def json_ld(data):
    j = jsonify(data)
    j.mimetype = "application/json"
    return j


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


@app.route("/navigation")
def navigation():
    collection = Collection.get_by_identifier(request.args.get("id"))

    if not collection:
        return json_error(title="Document not found",
                          message="This collection does not exist in our database.")

    if collection.collection_type != "Resource":
        return json_error(title="Document not readable",
                          message="This collection is not readable")

    if request.args.get("ref"):
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order == request.args.get("ref")
            )
        ).first()
        if not passages:
            return json_error(title="Passage not found", message="This passage was not found")

        # DTS Specification : Si je donne un passage, je dois récupérer ces enfants.
        #                     Nous ne gérons pas les enfants
        passages = []

    elif request.args.get("start") and request.args.get("end"):
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order.between(request.args.get("start"), request.args.get("end"))
            )
        ).all()
        if not passages:
            return json_error(title="Passage not found", message="This passage range was not found")

        # DTS Specification : Si je donne une range, je dois récupérer les enfants de la range
        #                     sauf si level=0 : je récupère les éléments entre les bornes
        if not request.args.get("level") or request.args.get("level") != "0":
            passages = []
    else:
        passages = collection.passages

    if request.args.get("groupBy"):
        group_by = request.args.get("groupBy")
        if not group_by.isnumeric():
            return json_error(
                title="Invalid groupBy value",
                message="The groupBy value is not a numerical one",
                code=400
            )
        group_by = int(group_by)
        if group_by == 0:
            return json_error(
                title="Invalid groupBy value",
                message="The groupBy value cannot be equal to 0",
                code=400
            )
        passages = grouper(n=group_by, iterable=passages)
        passages = [
            {"start": grouped[0].passage_order, "end": grouped[-1].passage_order}
            for grouped in passages
        ]
    else:
        passages = [{"ref": passage.passage_order} for passage in passages]

    return json_ld(
        {
            "@context": {
                "@vocab": "https://www.w3.org/ns/hydra/core#",
                "dc": "http://purl.org/dc/terms/",
                "dts": "https://w3id.org/dts/api#"
            },
            "@id": request.full_path,
            "dts:citeDepth": 1,
            "dts:level": 1,
            "member": passages,
            "dts:passage": url_for("document", id=collection.collection_identifier)+"{&ref}{&start}{&end}"
        }
    )
