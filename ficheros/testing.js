var fs = require('fs')
var i;
var path = '/home/liss/TFM/btn100/ficheros/';
var ver = fs.readdirSync(path);
var value, data, result;

for(i = 0; i < ver.length; i += 1){
	console.log(ver[i])
	if(ver[i].match(/ttl/)){
		value = path + ver[i];
		console.log(value)
		try{
			data = fs.readFileSync(value, 'utf8');
			result = data.replace(/\/_/g, '/').replace(/:_/g, ':');
			fs.writeFileSync(value,  result, 'utf8');
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
