from collections import defaultdict
from flask import render_template, request, Response, url_for, jsonify, redirect
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
def document_route():
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
def navigation_route():
    collection = Collection.get_by_identifier(request.args.get("id"))

    if not collection:
        return json_error(title="Collection not found",
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
            "dts:passage": url_for("document_route", id=collection.collection_identifier)+"{&ref}{&start}{&end}"
        }
    )


@app.route("/collection")
def collection_route():
    collection = Collection.get_by_identifier(request.args.get("id"))

    if not collection and request.args.get("id"):
        return json_error(title="Collection not found",
                          message="This collection does not exist in our database.")
    elif not collection:
        collection = Collection.query.filter(Collection.collection_parent==None).first()

    if request.args.get("nav", "children") == "children":
        members = collection.children
    else:
        members = [collection.parent]

    dc = defaultdict(list)
    extended = defaultdict(list)

    for triple in collection.triples:
        if triple.triple_predicate.startswith("http://purl.org/dc/terms/"):
            dc[triple.triple_predicate.replace("http://purl.org/dc/terms/", "dc:")].append(triple.triple_object)
        else:
            extended[triple.triple_predicate].append(triple.triple_object)

    data = {
        "@context": {
            "@vocab": "https://www.w3.org/ns/hydra/core#",
            "dc": "http://purl.org/dc/terms/",
            "dts": "https://w3id.org/dts/api#"
        },
        "@id": collection.collection_identifier,
        "@type": collection.collection_type,
        "totalItems": len(members),
        "title": collection.collection_title
    }

    if len(members):
        data["member"] = [
            {
                "@id": member.collection_identifier,
                "title": member.collection_title,
                "@type": member.collection_type,
                "totalItems": member.total_items
            }
            for member in members
        ]

    if dc:
        data["dts:dublincore"] = dc

    if extended:
        data["dts:extended"] = extended

    if collection.collection_type == "Resource":
        data.update({
            "dts:passage": url_for("document_route", id=collection.collection_identifier),
            "dts:references": url_for("navigation_route", id=collection.collection_identifier),
            "dts:citeDepth": 1
        })

    return json_ld(data)


@app.route("/")
def entry_point():
    return json_ld({
      "@context": "/dts/api/contexts/EntryPoint.jsonld",
      "@id": url_for("entry_point"),
      "@type": "EntryPoint",
      "collections": url_for("collection_route"),
      "documents": url_for("document_route"),
      "navigation": url_for("navigation_route")
    })


@app.route("/<path:path>")
def identifier_route(path):
    collection = Collection.get_by_identifier("/"+path)
    if not collection:
        return json_error(title="Collection not found",
                          message="This collection does not exist in our database.")
    return redirect(url_for("collection_route", id=collection.collection_identifier))
