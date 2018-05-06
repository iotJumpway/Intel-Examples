/*
    Title: ASL Classifier Socket Server Library
    Description: Sends frames of a webcam to the node js server via sockets.
    Last Modified: 2018-05-05
    
    Configuration:
    Update your socket server configuration in ../../required/confs.json 
*/

var socket = require('socket.io');
var io;

exports.listen = function(server,ip) {
    
    io = socket.listen(server,ip); 
    io.set('heartbeat interval', 2000000); 
    io.set('heartbeat timeout', 2000000);
    io.sockets.on('connection', function(socket) {
        
        socket.on('newFrame', function(img_location) {
            socket.broadcast.emit('newImage', { image_location : '/images/img.png' });
        });
    });
};