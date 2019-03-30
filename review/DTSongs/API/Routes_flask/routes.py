# On importe les modules Flask et render_template de la librairie flask.
from flask import Flask, render_template, jsonify
import xmltodict, json
from app import app

@app.route('/xml')
    return render_template('''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"
	schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Document de sortie XML</title>
         </titleStmt>
         <publicationStmt>
            <p/>
         </publicationStmt>
         <sourceDesc>
            <p/>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <p>'''for line in file.txt:'''</p>
      </body>
  </text>
</TEI>
'''), 200, {'Content-Type': 'application/xml'}

@app.route('/data_json')
def get_json():
    return print(json.dumps(xmltodict.parse('/xml')))