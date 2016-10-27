/**
 * Created by sachin on 27/10/16.
 */
'use strict';

var profileApp = profileApp || {};
profileApp.validator = {
    flag: 0,
    regexEmail: /^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$/,
    regexPassword: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/,
    inputElements: $('input'),
    errorSpan: $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>'),

    validateInput: function (input) {
        if (input.id === 'email') {
            return this.regexEmail.exec(input.value);
        }
        else if (input.id === 'password') {
            return this.regexPassword.exec(input.value);
        }
        else {
            return true;
        }
    },
    addErrorClass: function (currentParentElement) {
        currentParentElement.addClass('has-feedback has-error');
        this.errorSpan.appendTo(currentParentElement);
        this.flag += 1;
    },
    removeErrorClass: function (currentParentElement) {
        currentParentElement.removeClass('has-feedback has-error');
        currentParentElement.children().last().remove();
        this.flag -= 1;
    },
    validateInputElements: function () {
        var appObj = this;
        this.inputElements.each(function () {
            var currentParentElement = $(this).parent();

            if (!appObj.validateInput(this) && !currentParentElement.hasClass('has-error')) {
                appObj.addErrorClass(currentParentElement);
            }
            else if (appObj.validateInput(this) && currentParentElement.hasClass('has-error')) {
                appObj.removeErrorClass(currentParentElement);
            }
        });

        if (!appObj.flag && $("span").filter("#helpBlock").length) {
            var helpBlock = $('#helpBlock');
            helpBlock.parent().filter('#helpBlock').remove();
        }
        else if (appObj.flag && $("span").filter("#helpBlock").length === 0) {
            var helpSpan = $('<span id="helpBlock" class="help-block text-danger block-center">Please correct the columns with errors.</span>');
            helpSpan.insertBefore('#validate');
        }
    }
};

$(document).ready(function () {


    $('#validate').click(function () {
        profileApp.validator.validateInputElements();
        if (profileApp.validator.flag) {
            return false;
        }
        else {
            window.alert('Your data has been submitted successfully');
        }
    });


});
