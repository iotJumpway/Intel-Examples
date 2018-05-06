/*
    Title: ASL Classifier Socket Server
    Description: Sends frames of a webcam to the node js server via sockets.
    Last Modified: 2018-05-05
    
    Configuration:
    Update your socket server configuration in ../required/confs.json 
*/ 

var http = require('http');
var fs   = require('fs');
var path = require('path');
var mime = require('mime');
var url  = require('url');
var confs = require('../required/confs.json');

var PORT_NUMBER = confs.Cameras[0].SocketPort;

var server = http.createServer(function(request, response) {
    
    var filePath = false;
    if (request.url == '/') {
        filePath = './public/index.html';
    } else {
        filePath = './public' + url.parse(request.url).pathname;
    }
    
    serveStatic(response, filePath);
});

server.listen(PORT_NUMBER,confs.Cameras[0].SocketIP, function() {
    console.log("Server listening on port " + PORT_NUMBER);
});

function sendFrame(response, filePath, fileContents) {
    
    response.writeHead(
        200,
        {"Content-Type": mime.lookup(path.basename(filePath))}
    );
    response.end(fileContents);
}

function serveStatic(response, absPath) {
    fs.exists(absPath, function(exists) {
        
        if (exists) {
            
            fs.readFile(absPath, function(err, data) {
                if (err) {
                    send404(response);
                } else {
                    sendFrame(response, absPath, data);
                }
            });
        } else {
            send404(response);
        }
    });
}

function send404(response) {
    response.writeHead(404, {"Content-Type": 'text/plain'});
    response.write('Error 404: resource not found.');
    response.end();
}

var webcamServer = require('./lib/server');
webcamServer.listen(server);