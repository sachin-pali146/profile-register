'use strict';

var profileApp = profileApp || {};

profileApp.validator = {
    flag: 0,
    regexName: /^[a-zA-Z ]{2,30}$/,
    regexPhone: /^[0-9]{10}$/,
    regexAddress: /^[a-zA-Z0-9-_/: ]{2,50}$/,
    regexPin: /^[0-9]{6}$/,
    regexEmail: /^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$/,
    regexPassword: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/,
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
    passwordChecker: ['password', 'newPassword', 'oldPassword', 'confirmPassword'],
    setDefaultImage: function () {
        if ($('#prefix').val() === "master" || $('#prefix').val() === "mr") {
            $('#photo').attr('src', '../img/male.png');
        }
        else if ($('#prefix').val() === "miss" || $('#prefix').val() === "mrs") {
            $('#photo').attr('src', '../img/female.png');
        }
    },
    validateInput: function (input) {
        var result;
        if (this.nameChecker.indexOf(input.id) !== -1) {
            result = this.regexName.exec(input.value);
        }
        else if (this.addressChecker.indexOf(input.id) !== -1) {
            result = this.regexAddress.exec(input.value);
        }
        else if (this.phoneChecker.indexOf(input.id) !== -1) {
            result = this.regexPhone.exec(input.value);
        }
        else if (this.pinChecker.indexOf(input.id) !== -1) {
            result = this.regexPin.exec(input.value);
        }
        else if (input.id === 'dob') {
            var dobDate = new Date(input.value);
            result = dobDate < this.currentDate;
        }
        else if (input.id === 'email') {
            result = this.regexEmail.exec(input.value);
        }
        else if (this.passwordChecker.indexOf(input.id) !== -1) {
            result = this.regexPassword.exec(input.value);
        }
        else if (input.id === 'photo') {
            var photo = $('#photo').val();
            if (photo) {
                var supported_format = ["PNG", "JPG", "GIF", "JPEG"];
                var extension = supported_format.indexOf(photo.split('.').pop().toUpperCase());
                result = extension in supported_format;
            }
            else {
                this.setDefaultImage();
                result = true;
            }
        }

        else {
            result = true;
        }
        return result;
    },
    addErrorClass: function (currentParentElement) {
        currentParentElement.addClass('has-feedback has-error');
        $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
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
    },
    setData: function (user_data) {
        this.inputElements.each(function () {
            if (user_data[this.id]) {
                this.value = user_data[this.id];
            }
        });
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
    });
    $('#login,#submit').click(function () {
        profileApp.validator.validateInputElements();
        if (profileApp.validator.flag) {
            return false;
        }
    });

});

$(document).ready(function () {
    $('#profileDataSubmit').click(function () {
        //get file object
        var file = document.getElementById('profileFile').files[0];
        if (file) {
            // create reader
            var reader = new FileReader();
            reader.readAsText(file);
            reader.onload = function (value) {
                $.ajax({
                    type: "POST",
                    url: "http://localhost/read_data.py",
                    data: "profile=" + value.target.result,
                    success: function (result) {
                        var user_data = $.parseJSON(result);
                        profileApp.validator.setData(user_data);
                    }
                });
            };
        }
    });
});


