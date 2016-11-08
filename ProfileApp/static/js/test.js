var page = $.url('?page');
if (page === undefined) {
    page = '0';
}

$(document).ready(function () {
    function getUsers(_page) {

        $.ajax({
            url: 'http://localhost/user_data.py?page=' + _page,
            type: 'GET',
            success: function (res) {

    var itemsPerPage = 10;
    var urlpath = 'http://localhost/profiles.py?page='
    var userObj = JSON.parse(res);
    var total = userObj['total'];
    var pageCount = total / itemsPerPage;
    var pageRem = total % itemsPerPage;
    if (pageRem !== 0) {
        pageCount = Math.floor(pageCount) + 1;
    }

    $('#userTable > tbody').empty();
    $.each(userObj["data"], function (index) {
        $('#userTable >tbody').append("<tr><td>" + userObj['data'][index]['image_extension'] + "</td><td>" + userObj['data'][index]['firstName'] + "</td><td>" + userObj['data'][index]['lastName'] + "</td><td>" + userObj['data'][index]['employment'] + "</td><td>" + userObj['data'][index]['employer'] + "</td><td>" + userObj['data'][index]['email'] + "</td></tr>");

    });

    $('.pagination').empty();

    if (_page > 0) {
        var aPrev = $('<a/>').attr({
                'href': urlpath + (parseInt(_page) - 1).toString()
            }, {
                'aria-label': 'Previous'
            })
            .append($('<span/>').attr('aria-hidden', 'true').html('&laquo;'));

        $(aPrev).click(function () {
            getUsers(Number(_page) - 1);
        });

        var prevLink = $('<li/>').append(aPrev);
        $('.pagination').append(prevLink);
    }


    for (var i = 0; i < Number(pageCount); i++) {

        if (i > pageCount) {
            break;
        }

        var aPage = $('<a/>').attr('href', urlpath + i.toString()).text(i + 1);

        $(aPage).click(function (i) {
            return function () {
                getUsers(i);
            }
        }(i));
        var page = $('<li/>').append(aPage);

        if ((_page) === i) {
            $(page).attr('class', 'active');
        }

        $('.pagination').append(page);
    }

    if ((Number(_page) + 1) < pageCount) {
        var nextLink = $('<li/>').append($('<a/>').attr({
                'href': urlpath + (Number(_page) + 1)
            }, {
                'aria-label': 'Next'
            })
            .append($('<span/>').attr('aria-hidden', 'true').html('&raquo;').click(function () {
                getUsers(Number(_page) + 1);
            })));
        $('.pagination').append(nextLink);
    }
},
            error: function (error) {
                console.log(error);
            }
        });
    }

    getUsers(page)
})