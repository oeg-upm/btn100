# CONSULTAS

### ¿Cuáles son los municipios de la provincia ?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>

      SELECT DISTINCT ?codigoMunicipio ?nombreMunicipio WHERE {
        ?provincia a esadm:Provincia .
        ?provincia dc:title "Las Palmas" .
        ?provincia dc:title ?nombreProvincia .
        ?provincia geosparql:hasGeometry ?geoProv .
        ?geoProv geosparql:asWKT ?geoProvLocali .

        ?municipio a esadm:Municipio .
        ?municipio dc:title ?nombreMunicipio .
        ?municipio dc:identifier ?codigoMunicipio .
        ?municipio geosparql:hasGeometry ?geoMuni .
        ?geoMuni geosparql:asWKT ?geoMuniLocali .

        FILTER (bif:st_within(?geoMuniLocali, ?geoProvLocali)) .  

      } ORDER BY ASC(?nombreMunicipio) 



### Lugares de interés a 1km a la redonda del Núcleo de Población "Las Rozas de Madrid"

      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX btn100:<https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?nombre ?geoLugarLocali WHERE {
        ?nucleo a btn100:NucleoPoblacionSuperficial .
        ?nucleo dc:title "Las Rozas de Madrid" .
        ?nucleo geosparql:hasGeometry ?geoNucleo .
        ?geoNucleo geosparql:asWKT ?geoNucleoLocali .

        ?lugar a btn100:LugarDeInteres .
        ?lugar dc:title ?nombre .
        ?lugar geosparql:hasGeometry ?geoLugar .
        ?geoLugar geosparql:asWKT ?geoLugarLocali .

        FILTER (bif:st_intersects(?geoLugarLocali,?geoNucleoLocali,1))

      }ORDER by (?nombre)

### ¿Qué rios (lineales) cruzan el Parque Nacional de Sierra Nevada?

      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX btn100:<https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?nombre WHERE {
        ?parque a btn100:ParqueNacional .
        ?parque dc:title "Parque Nacional de Sierra Nevada" .
        ?parque geosparql:hasGeometry ?geoParque .
        ?geoParque geosparql:asWKT ?geoParqueLocali .

        ?rio a btn100:RioLineal .
        ?rio dc:title ?nombre .
        ?rio geosparql:hasGeometry ?geoRio .
        ?geoRio geosparql:asWKT ?geoRioLocali .

        FILTER (bif:st_within(?geoRioLocali,?geoParqueLocali))

      } ORDER by (?nombre)

### ¿Cual es la altitud del Pico Tibidabo?

      PREFIX btn100: <https://datos.ign.es/def/btn100#>
      PREFIX dc: <http://purl.org/dc/terms/>

      SELECT DISTINCT ?nombre ?cota WHERE {
        ?pico a btn100:Pico .
        ?pico dc:title "Pico Tibidabo" .
        ?pico dc:title ?nombre .
        ?pico btn100:cota ?cota .
      }


### ¿Cual es el pico de mayor altitud de España?

      PREFIX btn100: <https://datos.ign.es/def/btn100#>
      PREFIX dc: <http://purl.org/dc/terms/>

      SELECT DISTINCT ?nombre ?cota WHERE {
        ?pico a btn100:Pico .
        ?pico dc:title ?nombre .
        ?pico btn100:cota ?cota .
        
      } ORDER by DESC (xsd:integer(?cota)) LIMIT 1



### ¿Cual es el pico de mayor altitud de la Provincia de Madrid?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>

      SELECT DISTINCT ?nombre ?cota WHERE {
        ?provincia a esadm:Provincia .
        ?provincia dc:title "Madrid" .
        ?provincia dc:identifier ?codigoprovincia .
        ?provincia geosparql:hasGeometry ?geoProvincia .
        ?geoProvincia geosparql:asWKT ?geoProvinciaLocali .

        ?pico a btn100:Pico .
        ?pico dc:title ?nombre .
        ?pico btn100:cota ?cota .
        ?pico geosparql:hasGeometry ?geoPico .
        ?geoPico geosparql:asWKT ?geoPicoLocali .
        
        FILTER (bif:st_within(?geoPicoLocali, ?geoProvinciaLocali)) . 
        
      } ORDER BY DESC(xsd:integer(?cota)) LIMIT 1


### ¿Donde (nombre de municipio) están los aeropuertos en la Comunidad de Madrid?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?codigoMunicipio ?nombreMunicipio ?nombreAeropuerto WHERE {
        ?ccaa a esadm:ComunidadAutonoma .
        ?ccaa dc:title "Comunidad de Madrid" .
        ?ccaa geosparql:hasGeometry ?geoCCAA .
        ?geoCCAA geosparql:asWKT ?geoCCAALocali .

        ?municipio a esadm:Municipio .
        ?municipio dc:title ?nombreMunicipio .
        ?municipio dc:identifier ?codigoMunicipio .
        ?municipio geosparql:hasGeometry ?geoMuni .
        ?geoMuni geosparql:asWKT ?geoMuniLocali .

        FILTER (bif:st_intersects(?geoMuniLocali, ?geoCCAALocali))

        ?aeropuerto a btn100:Aeropuerto .
        ?aeropuerto dc:title ?nombreAeropuerto .
        ?aeropuerto geosparql:hasGeometry ?geoAero .
        ?geoAero geosparql:asWKT ?geoAeroLocali .

        FILTER (bif:st_intersects(?geoAeroLocali, ?geoMuniLocali))

      } ORDER BY ASC(?nombreMunicipio)


### ¿Por cuáles CCAA discurre el río Tajo?

      PREFIX btn100: <https://datos.ign.es/def/btn100#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>

      SELECT DISTINCT ?nombreCCAA WHERE {
        ?ccaa a esadm:ComunidadAutonoma .
        ?ccaa dc:title ?nombreCCAA .
        ?ccaa geosparql:hasGeometry ?geoCCAA .
        ?geoCCAA geosparql:asWKT ?geoCCAALocali .

        ?rio a btn100:RioLineal .
        ?rio dc:title "Río Tajo" .
        ?rio geosparql:hasGeometry ?geoRio .
        ?geoRio geosparql:asWKT ?geoRioLocali .

        FILTER (bif:st_intersects(?geoRioLocali, ?geoCCAALocali))
        
      } ORDER BY (?nombreCCAA)


### Municipios por los que pasa el Camino de Santiago "Catalán"

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?nombreMunicipio WHERE {
        ?camino a btn100:ItinerarioDeCaminoDeSantiago .
        ?camino dc:title "Camino Catalán" .
        ?camino geosparql:hasGeometry ?geoCamino .
        ?geoCamino geosparql:asWKT ?geoCaminoLocali .

        ?municipio a esadm:Municipio .
        ?municipio dc:title ?nombreMunicipio .
        ?municipio geosparql:hasGeometry ?geoMuni .
        ?geoMuni geosparql:asWKT ?geoMuniLocali .
        
        FILTER (bif:st_intersects(?geoCaminoLocali, ?geoMuniLocali))

      } ORDER BY (?nombreMunicipio)



### ¿Cuáles son las playas de la Provincia de Valencia?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?nombrePlaya ?geoPlayaLocali WHERE {
        ?provincia a esadm:Provincia .
        ?provincia dc:title "Barcelona" .
        ?provincia geosparql:hasGeometry ?geoProv .
        ?geoProv geosparql:asWKT ?geoProvLocali .

        ?playa a btn100:Playa .
        ?playa dc:title ?nombrePlaya .
        ?playa geosparql:hasGeometry ?geoPlaya .
        ?geoPlaya geosparql:asWKT ?geoPlayaLocali .
        
        FILTER (bif:st_intersects(?geoPlayaLocali, ?geoProvLocali))
        
      } ORDER BY (?nombrePlaya)

### ¿Qué líneas eléctricas atraviesan el municipio de Madrid?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?codigoLinea ?geoLineaLocali WHERE {
        ?municipio a esadm:Municipio .
        ?municipio dc:title "Madrid" .
        ?municipio geosparql:hasGeometry ?geoMuni .
        ?geoMuni geosparql:asWKT ?geoMuniLocali .

        ?linea a btn100:LineaElectricaDeBajaTension .
        ?linea dc:identifier ?codigoLinea .
        ?linea geosparql:hasGeometry ?geoLinea .
        ?geoLinea geosparql:asWKT ?geoLineaLocali .

        FILTER (bif:st_intersects(?geoLineaLocali, ?geoMuniLocali))

      } ORDER BY (?codigoLinea)


### ¿Qué vértices geodésicos hay en el municipio de Barcelona?

      PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
      PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
      PREFIX dc: <http://purl.org/dc/terms/>
      PREFIX btn100: <https://datos.ign.es/def/btn100#>

      SELECT DISTINCT ?codigoVertice ?nombreVertice WHERE {
        ?municipio a esadm:Municipio .
        ?municipio dc:title "Barcelona" .
        ?municipio geosparql:hasGeometry ?geoMuni .
        ?geoMuni geosparql:asWKT ?geoMuniLocali .

        ?vertice a btn100:VerticeGeodesicoDeOrdenInferior .
        ?vertice dc:identifier ?codigoVertice .
        ?vertice dc:title ?nombreVertice .
        ?linea geosparql:hasGeometry ?geoVertice .
        ?geoVertice geosparql:asWKT ?geoVerticeLocali .

        FILTER (bif:st_intersects(?geoVerticeLocali, ?geoMuniLocali))

      } ORDER BY (?nombreVertice)
