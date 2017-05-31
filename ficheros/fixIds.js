	var fs = require('fs')
var i;
var path = '/home/liss/TFM/btn100/ficheros/';
var ver = fs.readdirSync(path);
var value, data, result;

for(i = 0; i < ver.length; i += 1){
	if(ver[i].match(/ttl/)){
		value = path + ver[i];
		try{
			data = fs.readFileSync(value, 'utf8');
			var resourceName = data.match(/recurso\/(\w+)/);
			// var hasTitle = data.match(/dc:title/);
			var hasTitle = false;
			if(resourceName && !hasTitle/** && data.match(":_")**/){
				var vals = data.match(/georesource:\d+\s/g);
				for(var k = 0; k < vals.length; k += 1){
					data = data.replace(vals[k], vals[k].trim() + '>');
				}
				data = data.replace("georesource: ", "pandiak:");
				result = data.replace(/georesource:/g, "<http://geo.linkeddata.es/recurso/"+ resourceName[1] + "/")
				.replace(/\/_/g, '/').replace("pandiak:", "georesource: ");
				// .replace(/rdfs:label\s+\"/, "rdfs:label             \"" + resourceName[1] + '-' );
				fs.writeFileSync(value,  result, 'utf8');
			}

		}
		catch (e){
			console.log("ERROR " + value)
			console.log(e)
		}
	}
}


/**
var fs = require('fs')


fs.readFile('BTN100_0601L_AUTOVIA.ttl', 'utf8', function (err,data) {
if (err) {
return console.log(err);
}
var result = data.replace(/"</g, '<').replace(/>"@es/g, '>');

fs.writeFile('BTN100_0601L_AUTOVIA.ttl', result, 'utf8', function (err) {
if (err) return console.log(err);
});
});
**/
