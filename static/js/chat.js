// My JavaScript page

/* We define a variable 'text_box' for storing the html code structure of message that is displayed in the chat box. */
const text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
    '</div>';

let userState = '';

const userDiv = (senderId, receiverId, name, online) =>
    (`<a href="/chat/${senderId}/${receiverId}" id="user${receiverId}" class="collection-item row">
                    <img src="https://cdn1.iconfinder.com/data/icons/user-interface-203/76/icon-24-512.png" class="col s2">
                    <div class="col s10">
                    <span class="title" style="font-weight: bolder">${name}</span>
                    <span style="color: ${online ? 'green' : 'red'}; float: right">${online ? 'online' : 'offline'}</span>
                    </div>
                </a>`)

/* Send takes three args: sender, receiver, message. sender & receiver are ids of users, and message is the text to be sent. */
function send(sender, receiver, message) {
    //POST to '/api/messages', the data in JSON string format
    $.post('/api/messages/', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        var box = text_box.replace('{sender}', "You"); // Replace the text '{sender}' with 'You'
        box = box.replace('{message}', message); // Replace the text '{message}' with the message that has been sent.
        $('#board').append(box); // Render the message inside the chat-box by appending it at the end.
        scrolltoend(); // Scroll to the bottom of he chat-box
    })
}

/* Receive function sends a GET request to '/api/messages/<sender_id>/<receiver_id>' to get the list of messages. */
function receive() {
    // 'sender_id' and 'receiver_id' are global variables declared in the messages.html, which contains the ids of the users.
    $.get('/api/messages/' + sender_id + '/' + receiver_id, function (data) {
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}

/* Register function takes two arguments: username and password, for creating the user. */
function register(username, password) {
     // Post to '/api/users' for creating a user, the data in JSON string format.
    $.post('/api/users/', '{"username": "'+ username +'", "password": "'+ password +'"}',
        function (data) {
            window.location = '/';  // Redirect to login page if success
        }).fail(function (response) {
            $('#id_username').addClass('invalid');  // Add class 'invalid' which will display "Username already taken" in the registration form if failed
        })
}

/* Keep the latest message view-able without scrolling each time it arrives */
function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}


function getUsers(senderId, callback) {
    return $.get('/api/users', function (data) {
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                console.log(user);
                if (user.id === senderId) {
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.username, user.online), ...res]
                }
            }, []);
            callback(doc)
        }
    })
}