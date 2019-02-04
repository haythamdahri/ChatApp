





    var chat_windows_id = [];


    function add_chat_window(user_id) {
        chat_windows_id.unshift(user_id);
    }

    function remove_chat_window(user_id) {
        chat_windows_id.splice($.inArray(user_id, chat_windows_id), 1);
    }

    function display_chat_window() {
        var i = 220; // start position
        var j = 310;  //next position
        $.each(chat_windows_id, function (index, value) {
            if (index < 3) {
                $("#chatwindow" + value).css({'right': i});
                $("#chatwindow" + value).show();
                i += j;
            } else {
                $("#chatwindow" + value).hide();
            }
        });
    }


    $("body").delegate(".chatbox__message", 'focus', function (e) {
       console.log($(this).attr('id'));
       console.log("User id: "+$(this).data('user_id'));
       var user_id = $(this).data('user_id');
       var url_receiver = $(this).attr('url_receiver');
       var csrf_token = $(this).attr('csrf_token');
       read_messages(user_id, url_receiver, csrf_token);
    });

    function read_messages(user_id, url_receiver, csrf_token){
        $.ajax({
            type: "POST",
            url: url_receiver,
            data: {'user_id': user_id, 'csrfmiddlewaretoken': csrf_token},
            dataType: 'json',
            success: function (response) {
                if( response.status && response.unread_messages_counter == 0 ) {
                    if ($("body").children("#unread_messages" + user_id).css('display') != "none") {
                        console.log("counter: " + response.unread_messages_counter);
                        $("body").find("#unread_messages" + user_id).hide();
                        $("body").find("#unread_messages" + user_id).text("");
                        console.log("User_id: "+user_id);
                    } else {
                        $("body").find("#unread_messages" + user_id).show();
                        $("body").find("#unread_messages" + user_id).text(response.unread_messages_counter);
                        console.log("User_id: "+user_id);
                    }
                }
            },
            complete: function (response) {

            },
            error: function (response) {
                swal('error', 'try again', 'error');
            }
        });

    }


    function get_unread_message(userID, url_mask){
        $.ajax({
            type: "GET",
            url: url_mask,
            data: {'user_id': userID},
            dataType: 'json',
            success: function (response) {
                if( response.unread_messages_count > 0 ){
                    $("#unread_messages"+userID).show();
                    $("#unread_messages"+userID).text(response.unread_messages_count);
                }else{
                    $("#unread_messages"+userID).hide();
                    $("#unread_messages"+userID).text("");
                }
            },
            complete: function (response) {
                display_chat_window();
            },
            error: function (response) {
                swal('error', 'try again', 'error');
            }
        });
    }

    $(document).on('click', '#sidebar-user-box', function () {

        var userID = $(this).data('id');
        var username = $(this).children().text();
        console.log(userID);
        /*
                if ($.inArray(userID, arr) != -1) {
                    arr.splice($.inArray(userID, arr), 1);
                }

                arr.unshift(userID);*/
        var url_mask = $(this).attr('url_receiver');
        var csrf_token = $(this).attr('csrf');
        var url_unread_messages = $(this).attr('url_unread_messages');
        console.log(csrf_token);
        console.log(url_mask);
        $.ajax({
            type: "POST",
            url: url_mask,
            data: {'user_id': userID, 'csrfmiddlewaretoken': csrf_token},
            dataType: 'json',
            success: function (response) {
                if ($.inArray(userID, chat_windows_id) == -1) {
                    add_chat_window(userID);
                } else {
                    $("#chatwindow" + userID).remove();
                    chat_windows_id.splice($.inArray(userID, chat_windows_id), 1);
                    add_chat_window(userID);
                }
                $("body").append(response);
                get_unread_message(userID, url_unread_messages);
            },
            complete: function (response) {
                display_chat_window();
            },
            error: function (response) {
                swal('error', 'try again', 'error');
            }
        });

    });

