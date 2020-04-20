"use strict";

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

$(document).ready(function () {
    "use strict";

    var $todoListButton = $(".ul-contact-mobile-icon");
    var $todoSidebar = $(".ul-todo-sidebar");
    var $todoSidebarClose = $(".todo-sidebar-close ");

    $todoListButton.on("click", function () {
        $todoSidebar.addClass('ul-todo-sidebar open');
    });

    $todoSidebarClose.on("click", function () {
        $todoSidebar.removeClass(' open');
    });

    // CRUD operation 
    var persons = [{
        id: 1,
        img: "assets/images/faces/1.jpg"
    }, {
        id: 2,
        img: "assets/images/faces/2.jpg"
    }, {
        id: 3,
        img: "assets/images/faces/3.jpg"
    }, {
        id: 4,
        img: "assets/images/faces/4.jpg"
    }];
    var users = [{
        id: 1,
        title: "Bob",
        img: "assets/images/faces/1.jpg",
        badge: "<span href=\"#\" class=\"badge badge-warning mr-2\">Test</span>"

    }, {
        id: 2,
        title: "Harry",
        img: "assets/images/faces/2.jpg"

    }, {
        id: 3,
        title: "Bob",
        img: "assets/images/faces/3.jpg"

    }, {
        id: 4,
        title: "Harry",
        img: "assets/images/faces/4.jpg"

    }];

    $('#todo-list-search').keyup(function () {
        search_table($(this).val());
    });
    function search_table(value) {
        $('#userTable li').each(function () {
            var found = 'false';
            $(this).each(function () {
                if ($(this).text().toLowerCase().indexOf(value.toLowerCase()) >= 0) {
                    found = 'true';
                }
                if (found == 'true') {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });
    }

    $("form").submit(function (e) {
        e.preventDefault();
    });

    $.each(users, function (i, user) {
        appendToUserTable(user);
    });

    function addUser(user) {
        users.push(user);
        appendToUserTable(user);
    };

    $("form#addUser").submit(function () {
        var modifiedUser = {};
        var nameInput = $('input[name="title"]').val();
        var addressInput = $('textarea[name="description"]').val();
        var selectOption = $(this).find(':selected').val();
        var person = persons.filter(function (person) {
            return person.id == selectOption;
        });

        if (nameInput && addressInput && selectOption != 0) {
            $(this).serializeArray().map(function (data) {
                modifiedUser[data.name] = data.value;
                modifiedUser = _extends({}, modifiedUser, person[0]);
            });
            console.log(modifiedUser);
            addUser(modifiedUser);
            this.reset();
        } else {
            alert('All fields must have a valid value.');
        }
    });

    function appendToUserTable(user) {
        $("#userTable").append("<li class=\"list-group-item\">\n        <div class=\"ul-todo-title-wrapper d-flex justify-content-between align-items-center\">\n            <div  class=\"ul-todo-area d-flex\">\n                <div>\n                    <label class=\"checkbox checkbox-primary\">\n                        <input type=\"checkbox\">\n                \n                        <span class=\"checkmark\"></span>\n                    </label>\n                </div>\n                <div>\n                    " + user.title + "\n                </div>\n               \n            </div>\n            \n            <div class=\"ul-todo-action d-flex align-items-center\">\n            \n            <span href=\"#\" class=\"badge badge-danger mr-2\">Developer</span>\n            <span href=\"#\" class=\"badge badge-warning mr-2\">UI/UX</span>\n                <div class=\"ul-widget4__img\">\n                    <img src=\"" + user.img + "\" class=\"rounded-circle\" id=\"userDropdown\" alt=\"\" data-toggle=\"dropdown\"\n                        aria-haspopup=\"true\" aria-expanded=\"false\">\n                </div>\n                <button type=\"button\" class=\"btn bg-transparent _r_btn border-0\" data-toggle=\"dropdown\" aria-haspopup=\"true\"\n                    aria-expanded=\"false\">\n                    <span class=\"_dot _r_block-dot bg-dark\"></span>\n                    <span class=\"_dot _r_block-dot bg-dark\"></span>\n                    <span class=\"_dot _r_block-dot bg-dark\"></span>\n                </button>\n                <div class=\"dropdown-menu\" x-placement=\"bottom-start\">\n                    <a class=\"dropdown-item\" href=\"#\"><i class=\"nav-icon i-Pen-2 text-success font-weight-bold mr-2\"></i>Edit\n                        Contact</a>\n                    <a class=\"dropdown-item\" href=\"#\"><i class=\"nav-icon i-Close-Window text-danger font-weight-bold mr-2\"></i>Delete\n                        Contact</a>\n                </div>\n            </div>\n        </div>\n    </li>");
    }
});