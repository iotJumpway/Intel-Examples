var socket = io.connect();

socket.on('newImage', function (data) {
    
    $('#streamHolder').attr('src', data.image_location + '?time=' + new Date().getTime());

}); 