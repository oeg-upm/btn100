# CONSULTAS

### Obtener los albergues 1km a la redonda de los itinerarios

    SELECT DISTINCT ?pname ?aname
    WHERE {
      ?albergue rdf:type geoes:Albergue.
      ?albergue dc:title ?aname.
      ?albergue geosparql:hasGeometry ?ageo .
      ?ageo geosparql:asWKT ?apos .
      ?s rdf:type geoes:ItinerarioDeCaminoDeSantiago.
      ?s dc:title ?pname.
      ?s geosparql:hasGeometry ?pgeo .
      ?pgeo geosparql:asWKT ?w .
      FILTER (bif:st intersects (?apos, ?w, 1))
    }
    ORDER BY ASC(?pname)
### Obtener las comunidades autónomas donde están situados los aeropuertos
      SELECT ?comunidad ?aeropuerto
      WHERE {
        ?c rdf:type geoes:ComunidadAutonoma.
        ?c dc:title ?comunidad.
        ?c geosparql:hasGeometry ?cgeo.
        ?cgeo geosparql:asWKT ?cpos.
        ?a rdf:type geoes:Aeropuerto.
        ?a dc:title ?aeropuerto.
        ?a geosparql:hasGeometry ?ageo.
        ?ageo geosparql:asWKT ?apos.
        FILTER (bif:st within(?cpos,?apos)).
      }
      ORDER BY DESC(?cname)

### Obtener los puntos de interés que estén a 5km a la redonda de sol

      SELECT DISTINCT (bif:st distance(bif:st point(-3.7035, 40.4169), ?ca pos)) as ?distance
      ?title
      WHERE {
        ?ca rdf:type geoes:LugarDeInteres.
        ?ca dc:title ?title .
        ?ca geosparql:hasGeometry ?ca geo .
        ?ca geo geosparql:asWKT ?ca pos .
        FILTER (bif:st intersects (bif:st point(-3.7035, 40.4169), ?ca pos, 5)) .
      }
      ORDER BY ASC(?distance)

### Obtener el número de playas por provincia

      SELECT DISTINCT count(*) as ?count ?pname

      WHERE {
        ?provincia rdf:type geoes:Provincia.
        ?provincia dc:title ?pname.
        ?provincia geosparql:hasGeometry ?pgeo .
        ?pgeo geosparql:asWKT ?ppos .
        ?playa rdf:type geoes:Playa.
        ?playa dc:title ?plname .
        ?playa geosparql:hasGeometry ?plgeo .
        ?plgeo geosparql:asWKT ?plpos .
        FILTER (bif:st within(?ppos, ?plpos)) .
      }
      GROUP BY ?pname
      ORDER BY DESC(?count)


### Provincia con el mayor número de playas

      SELECT DISTINCT MAX (?count) as ?playas ?pname
      WHERE {
        FILTER(?count >= 93)
        {
        SELECT DISTINCT count(*) as ?count ?pname
          WHERE {
            ?provincia rdf:type geoes:Provincia.
            ?provincia dc:title ?pname.
            ?provincia geosparql:hasGeometry ?pgeo .
            ?pgeo geosparql:asWKT ?ppos .
            ?playa rdf:type geoes:Playa.
            ?playa dc:title ?plname .
            ?playa geosparql:hasGeometry ?plgeo .
            ?plgeo geosparql:asWKT ?plpos .
            FILTER (bif:st within(?ppos, ?plpos)) .
          }
        }
      }

### Obtener una descripción más detallada de un aeropuerto en dbpedia

      prefix dbpedia: <http://dbpedia.org/resource/>
      prefix dbpedia-owl: <http://dbpedia.org/ontology/>
      SELECT *
      WHERE {
        ?myairport rdf:type geoes:Aeropuerto.
        ?myairport owl:sameAs ?dbpedia airport.
        filter (regex(str(?dbpedia airport), “ˆ(http://dbpedia.org/resource/)([a-z]| |-)+$”, “i”)).
        SERVICE <http://dbpedia.org/sparql> {
          ?dbpedia airport rdfs:comment ?comment.
          FILTER langMatches(lang(?comment), “es”).
        }
      }


### obtener la provincia con mas playas en españa

      SELECT distinct MAX (?count) ?pname WHERE{
          FILTER(?count >= 93)
          {
            SELECT distinct count(*) as ?count ?pname
             where{
               ?provincia rdf:type geoes:Provincia.
               ?provincia dc:title ?pname.
               ?provincia geosparql:hasGeometry ?pgeo .
               ?pgeo geosparql:asWKT ?ppos .

               ?playa rdf:type geoes:Playa.
               ?playa dc:title ?plname .
               ?playa geosparql:hasGeometry ?plgeo .
               ?plgeo geosparql:asWKT ?plpos .
               FILTER (bif:st_within(?ppos, ?plpos)) .
             }
        }
      }


### obterner los puntos de interes que esten a 5 km a la redonda del aeropuerto de Madrid.

      SELECT distinct ?title (bif:st_distance(?lpos, ?ca_pos))  as ?distance where{
        ?l rdf:type geoes:Aeropuerto.
        ?l dc:title "Aeropuerto de Adolfo Suárez Madrid-Barajas"@es .
        ?l geosparql:hasGeometry ?lgeo .
        ?lgeo geosparql:asWKT ?lpos .

        ?ca rdf:type geoes:LugarDeInteres.
        ?ca dc:title ?title .
        ?ca geosparql:hasGeometry ?ca_geo .
        ?ca_geo geosparql:asWKT ?ca_pos .

        FILTER (bif:st_intersects (?lpos, ?ca_pos, 5)) .
      }
