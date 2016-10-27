'use strict';

var profileApp = profileApp || {};

profileApp.validator = {
    flag: 0,
    regexName: /^[a-zA-Z ]{2,30}$/,
    regexPhone: /^[0-9]{10}$/,
    regexAddress: /^[a-zA-Z0-9-_/: ]{2,50}$/,
    regexPin: /^[0-9]{6}$/,
    checkboxAddress: $('#checkboxAddress'),
    dob: $('#dob'),
    currentDate: new Date(),
    homeStreet: $('#homeStreet'),
    homeCity: $('#homeCity'),
    homeState: $('#homeState'),
    homePhone: $('#homePhone'),
    homePin: $('#homePin'),
    homeFax: $('#homeFax'),
    officeStreet: $('#officeStreet'),
    officeCity: $('#officeCity'),
    officeState: $('#officeState'),
    officePhone: $('#officePhone'),
    officePin: $('#officePin'),
    officeFax: $('#officeFax'),
    inputElements: $('input'),
    nameChecker: ['firstName', 'lastName', 'homeCity', 'homeState', 'officeState',
        'employer', 'employment', 'officeCity'],
    phoneChecker: ['homePhone', 'homeFax', 'officePhone', 'officeFax'],
    addressChecker: ['homeStreet', 'officeStreet'],
    pinChecker: ['homePin', 'officePin'],
    errorSpan: $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>'),

    validateInput: function (input) {
        if (this.nameChecker.indexOf(input.id) !== -1) {
            return this.regexName.exec(input.value);
        }
        else if (this.addressChecker.indexOf(input.id) !== -1) {
            return this.regexAddress.exec(input.value);
        }
        else if (this.phoneChecker.indexOf(input.id) !== -1) {
            return this.regexPhone.exec(input.value);
        }
        else if (this.pinChecker.indexOf(input.id) !== -1) {
            return this.regexPin.exec(input.value);
        }
        else if (input.id === 'dob') {
            var dobDate = new Date(input.value);
            return dobDate < this.currentDate;
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
    checkAddress: function () {
        if (this.checkboxAddress.prop('checked')) {
            $('#officeAddress').prop('disabled', true);
            this.officeStreet.val(this.homeStreet.val());
            this.officeCity.val(this.homeCity.val());
            this.officeState.val(this.homeState.val());
            this.officePin.val(this.homePin.val());
            this.officePhone.val(this.homePhone.val());
            this.officeFax.val(this.homeFax.val());
        }
        else {
            $('#officeAddress').prop('disabled', false);
        }
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

    $('#checkboxAddress').change(function () {
        profileApp.validator.checkAddress();
    });

    $('#validate').click(function () {
        profileApp.validator.checkAddress();
        profileApp.validator.validateInputElements();
        if (profileApp.validator.flag) {
            return false;
        }
        else {
            window.alert('Your data has been submitted successfully');
        }
    });


});



