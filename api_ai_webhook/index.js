/*
* HTTP Cloud Function.
*
* @param {Object} req Cloud Function request context.
* @param {Object} res Cloud Function response context.
*/

'use strict';
const http = require('http');
const host = '';
const port = '80';
exports.govhackWebhook = (req, res) => {
	let city = req.body.result.parameters['geo-city']; // city is a required param

	let date = '';
	if (req.body.result.parameters['date']) {
	  date = req.body.result.parameters['date'];
	  console.log('Date: ' + date);
	}
	
	let tag = '';
	if (req.body.result.parameters['tag']) {
	  tag = req.body.result.parameters['tag'];
	  console.log('Tag: ' + tag);
	}
	
	callPythonApi(city, date, tag).then((output) => {
		res.setHeader('Content-Type', 'application/json');
		res.send(JSON.stringify({ 'speech': output, 'displayText': output }));
	}).catch((error) => {
		res.setHeader('Content-Type', 'application/json');
		res.send(JSON.stringify({ 'speech': error, 'displayText': error }));
	});
};


function callPythonApi (city, date, tag) {
	return new Promise((resolve, reject) => {
		let path = '&format=json&city=' + encodeURIComponent(city) + '&tag=' + encodeURIComponent(tag) + '&date=' + date;
		console.log('API Request: ' + host + path + port);

		http.get({host: host, path: path, port: port}, (res) => {
			let body = ''; // var to store the response chunks
			res.on('data', (d) => { body += d; }); // store each response chunk
			res.on('end', () => {
				// After all the data has been received parse the JSON for desired
				// data
				let response = JSON.parse(body);
				// Create response
				let description = response['description'];
				let start = response['start'];
				let finish = response['finish'];
				let title = response['title'];
				let web = response['web'];
		        
				let output = '';
				if (title == "none") {
					output = `There are no events listed of type ${tag} in ${city}`;
				} else {
					output = `The event ${title} described as ${description} starts at ${start} and ends at ${finish}. The website ${web} for more information.`;
				}
					
				// Resolve the promise with the output text
				console.log(output);
				resolve(output);
			
			});
			res.on('error', (error) => {
				reject(error);
			});
		});
	});
}



