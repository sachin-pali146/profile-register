'use strict';

var profileApp = profileApp || {};

profileApp.validator = {
    flag: 1,
    regexName: /^[a-zA-Z ]{2,30}$/,
    regexPhone: /^[0-9]{10}$/,
    regexAddress: /^[a-zA-Z0-9-_/: ]{2,50}$/,
    regexPin: /^[0-9]{6}$/,
    inputElements: document.getElementsByTagName('input'),
    nameChecker: ['firstName', 'lastName', 'homeCity', 'homeState', 'officeState',
        'employer', 'employment', 'officeCity'],
    phoneChecker: ['homePhone', 'homeFax', 'officePhone', 'officeFax'],
    addressChecker: ['homeStreet', 'officeStreet'],
    pinChecker: ['homePin', 'officePin'],
    errorSpan: document.createElement('span'),

    validateName: function (nameInput) {
        return this.regexName.exec(nameInput.value);
    },
    validatePhone: function (phoneInput) {
        return this.regexPhone.exec(phoneInput.value);
    },
    validatePin: function (pinInput) {
        return this.regexPin.exec(pinInput.value);
    },
    validateAddress: function (addressInput) {
        return this.regexAddress.exec(addressInput.value);
    },
    validateInputElements: function () {

        for (var i = 0; i < this.inputElements.length; i++) {
            var currentParentElement = this.inputElements[i].parentElement;
            if (this.nameChecker.indexOf(this.inputElements[i].id) !== -1) {
                if (!this.validateName(this.inputElements[i])) {

                    currentParentElement.classList.add('has-feedback');
                    currentParentElement.classList.add('has-error');
                    $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
                    this.flag = 0;
                }
                else if (currentParentElement.classList.contains('has-error')) {
                    currentParentElement.classList.remove('has-feedback');
                    currentParentElement.classList.remove('has-error');
                    currentParentElement.removeChild(currentParentElement.childNodes[currentParentElement.childNodes.length - 1]);
                }
            }
            else if (this.phoneChecker.indexOf(this.inputElements[i].id) !== -1) {
                if (!this.validatePhone(this.inputElements[i])) {

                    currentParentElement.classList.add('has-feedback');
                    currentParentElement.classList.add('has-error');
                    $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
                    this.flag = 0;

                }
                else if (currentParentElement.classList.contains('has-error')) {
                    currentParentElement.classList.remove('has-feedback');
                    currentParentElement.classList.remove('has-error');
                    currentParentElement.removeChild(currentParentElement.childNodes[currentParentElement.childNodes.length - 1]);
                }
            }
            else if (this.addressChecker.indexOf(this.inputElements[i].id) !== -1) {
                if (!this.validateAddress(this.inputElements[i])) {

                    currentParentElement.classList.add('has-feedback');
                    currentParentElement.classList.add('has-error');
                    $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
                    this.flag = 0;

                }
                else if (currentParentElement.classList.contains('has-error')) {
                    currentParentElement.classList.remove('has-feedback');
                    currentParentElement.classList.remove('has-error');
                    currentParentElement.removeChild(currentParentElement.childNodes[currentParentElement.childNodes.length - 1]);
                }
            }
            else if (this.pinChecker.indexOf(this.inputElements[i].id) !== -1) {
                if (!this.validatePin(this.inputElements[i])) {

                    currentParentElement.classList.add('has-feedback');
                    currentParentElement.classList.add('has-error');
                    $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
                    this.flag = 0;

                }
                else if (currentParentElement.classList.contains('has-error')) {
                    currentParentElement.classList.remove('has-feedback');
                    currentParentElement.classList.remove('has-error');
                    currentParentElement.removeChild(currentParentElement.childNodes[currentParentElement.childNodes.length - 1]);
                }
            }

        }


    }
}

document.getElementById('validate').onclick = function () {
    profileApp.validator.validateInputElements();
    if (!profileApp.validator.flag) {
        return false;
    }
}



