# Importation du module defaultdict depuis la librairie collection.
from collections import defaultdict
# Importation des modules render_templates, request, Response, url_for, jsonify et redirect à partir de la librairie flask.
from flask import render_template, request, Response, url_for, jsonify, redirect
# Appel des fonctions app et db depuis le module .app
from .app import app, db
# Appel des classes passage et collection depuis le module .models
from .models import Passage, Collection

# Fonction qui créer la réponse 404 lorsque le XML n'est pas trouvé dans l'app.
def not_found_xml(response):
    # La fonction retourne un objet response contenant une réponse,
    # un status et cette réponse est un mimetype XML.
    return Response(
        response,
        status=404,
        mimetype="text/xml"
    )

# Défintion de la fonction de réponse à une erreur JSON,
# la réponse à l'erreur est elle-même donné au format JSON.
def json_error(title, message, code=404):
    # Création de la variable j dans laquelle on stocke le
    # contenu de la réponse que l'on passe au format json avec jsonify.
    j = jsonify({
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@type": "Status",
      "statusCode": code,
      "title": title,
      "description": message,
    })
    # On retourne le réponse j et le code de la réponse.
    return j, code

# Fonction qui permet de donner la position d'un identifiant dans une liste.
def grouper(n, iterable):
    """ Group a sequence (iterable) into a sequence of n

    :param n: Grouping size
    :param iterable: List of identifiers
    :yield: List of list of size N
    """
    # pour une position dans le range 0 taille de l'itérable, on donne l'itérable
    # comme la position augmenté de n.
    for pos in range(0, len(iterable), n):
        # yield a la même fonction que return mais il est utilisé dans le cadre des itérable.
        yield iterable[pos:pos + n]

# Fonction qui créé un élément json à partir de données passées en argument de la fonction.
def json_ld(data):
    # on stocke dans j les données passées au format json avec jsonify.
    j = jsonify(data)
    j.mimetype = "application/json"
    # on retourne j
    return j

# Définiton des routes de l'application.
@app.route("/document")
# Fonction qui donne le endpoint Document.
def document_route():
    # on récupère les collections leur ID.
    collection = Collection.get_by_identifier(request.args.get("id"))
    # Si on ne trouve pas de collection
    if not collection:
        # on retourne la réponse error.xml avec un titre et un message.
        return not_found_xml(
            render_template("error.xml", code=404, title="Document not found",
                            message="This collection does not exist in our database.")
        )
# si le type de la collection n'est pas "Resource"
    if collection.collection_type != "Resource":
        return not_found_xml(
            render_template("error.xml", code=404, title="Document not readable",
                            message="This collection is not readable")
        )
# si on récupère un ref,
    if request.args.get("ref"):
        # on filtre passage par ID dans collection et par ordre de ref.
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order == request.args.get("ref")
            )
            # on ne récpuère que le premier résultat.
        ).first()
        # si on ne trouve pas de passage,
        if not passages:
            # on renvoie un message d'erreur: la template error.xml
            return not_found_xml(
                render_template("error.xml", code=404, title="Passage not found", message="This passage was not found")
            )
        # on stocke la liste des passages dans un liste passage.
        passages = [passages]
        # si on récupère un start et un end,
    elif request.args.get("start") and request.args.get("end"):
        # on filtre passage par id de collection et par ordre entre le start et le end.
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order.between(request.args.get("start"), request.args.get("end"))
            )
            # on récupère tous les résultats.
        ).all()
        # s'il n'y a pas de passage,
        if not passages:
            # on retourne une erreur: le template error.xml.
            return not_found_xml(
                render_template("error.xml", code=404, title="Passage not found", message="This passage range"
                                                                                          " was not found")
            )
        # dans les autres cas, on récupère, dans collection, les passages.
    else:
        passages = collection.passages
# la fonction retourne une réponse: le template tei.xml avec la collection et les passages.
    return Response(
        render_template(
            "tei.xml",
            collection=collection,
            passages=passages
        ),
        # on précise le mimetype de la réponse: un fichier xml
        mimetype="text/xml"
    )

# Définition de la route du endpoint navigation.
@app.route("/navigation")
# Fonction du endpoint navigation, on requête la Collection par identifiant.
def navigation_route():
    # on requête les collections par identifiant.
    collection = Collection.get_by_identifier(request.args.get("id"))
# si on ne trouve pas de collection,
    if not collection:
        # on retourne une erreur json portant un titre et un message.
        return json_error(title="Collection not found",
                          message="This collection does not exist in our database.")
# si le type de la collection n'est pas ressource:
    if collection.collection_type != "Resource":
        # on retourne une erreur json.
        return json_error(title="Document not readable",
                          message="This collection is not readable")
# si on récupère des ref
    if request.args.get("ref"):
        # on filtre les passage par id de collection et par ordre de passage.
        passages = Passage.query.filter(
            db.and_(
                Passage.passage_collection == collection.collection_id,
                Passage.passage_order == request.args.get("ref")
            )
            # on récupère le premier résultat.
        ).first()
        # si on ne trouve pas de passage,
        if not passages:
            # on retourne une erreur json.
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
