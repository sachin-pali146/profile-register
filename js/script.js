'use strict';

var profileApp = profileApp || {};

profileApp.validator = {
    flag: 0,
    regexName: /^[a-zA-Z ]{2,30}$/,
    regexPhone: /^[0-9]{10}$/,
    regexAddress: /^[a-zA-Z0-9-_/: ]{2,50}$/,
    regexPin: /^[0-9]{6}$/,
    checkboxAddress: document.getElementById('checkboxAddress'),
    dob: document.getElementById('dob'),
    currentDate: new Date(),
    homeStreet: document.getElementById('homeStreet'),
    homeCity: document.getElementById('homeCity'),
    homeState: document.getElementById('homeState'),
    homePhone: document.getElementById('homePhone'),
    homePin: document.getElementById('homePin'),
    homeFax: document.getElementById('homeFax'),
    officeStreet: document.getElementById('officeStreet'),
    officeCity: document.getElementById('officeCity'),
    officeState: document.getElementById('officeState'),
    officePhone: document.getElementById('officePhone'),
    officePin: document.getElementById('officePin'),
    officeFax: document.getElementById('officeFax'),
    inputElements: document.getElementsByTagName('input'),
    nameChecker: ['firstName', 'lastName', 'homeCity', 'homeState', 'officeState',
        'employer', 'employment', 'officeCity'],
    phoneChecker: ['homePhone', 'homeFax', 'officePhone', 'officeFax'],
    addressChecker: ['homeStreet', 'officeStreet'],
    pinChecker: ['homePin', 'officePin'],
    errorSpan: document.createElement('span'),

    validateInput: function (input) {
        if (this.nameChecker.indexOf(input.id) !== -1) {
            return this.regexName.exec(input.value);
        }
        else if (this.addressChecker.indexOf(input) !== -1) {
            return this.regexAddress.exec(input.value);
        }
        else if (this.phoneChecker.indexOf(input) !== -1) {
            return this.regexPhone.exec(input.value);
        }
        else if (this.pinChecker.indexOf(input) !== -1) {
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
        currentParentElement.classList.add('has-feedback');
        currentParentElement.classList.add('has-error');
        $('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>').appendTo(currentParentElement);
        this.flag += 1;
    },
    removeErrorClass: function (currentParentElement) {
        currentParentElement.classList.remove('has-feedback');
        currentParentElement.classList.remove('has-error');
        currentParentElement.removeChild(currentParentElement.childNodes[currentParentElement.childNodes.length - 1]);
        this.flag -= 1;
    },
    checkAddress: function () {
        if (this.checkboxAddress.checked) {
            document.getElementById('officeAddress').disabled = true;
            this.officeStreet.value = this.homeStreet.value;
            this.officeCity.value = this.homeCity.value;
            this.officeState.value = this.homeState.value;
            this.officePin.value = this.homePin.value;
            this.officePhone.value = this.homePhone.value;
            this.officeFax.value = this.homeFax.value;
        }
        else {
            document.getElementById('officeAddress').disabled = false;
        }
    },
    validateInputElements: function () {
        var inputElementLength = this.inputElements.length;
        for (var i = 0; i < inputElementLength; i++) {
            var currentParentElement = this.inputElements[i].parentElement;

            if (!this.validateInput(this.inputElements[i]) && (!currentParentElement.classList.contains('has-error'))) {
                this.addErrorClass(currentParentElement);
            }
            else if (this.validateInput(this.inputElements[i]) && (currentParentElement.classList.contains('has-error'))) {
                this.removeErrorClass(currentParentElement);
            }

        }

        if (!this.flag) {
            var helpBlock = document.getElementById('helpBlock');
            
            if (helpBlock) {
                helpBlock.parentElement.removeChild(helpBlock);
            }
        }
        else if (!document.getElementById('helpBlock')) {
            var helpSpan = document.createElement("span");
            helpSpan.innerHTML = '<span id="helpBlock" class="help-block text-danger block-center">Please correct the columns with errors.</span>';
            var validate = document.getElementById('validate');
            validate.parentElement.insertBefore(helpSpan, validate);
        }
    }
};

document.getElementById('validate').onclick = function () {
    profileApp.validator.checkAddress();
    profileApp.validator.validateInputElements();
    if (profileApp.validator.flag) {
        return false;
    }
    else {
        window.alert('Your data has been submitted successfully');
    }
};

document.getElementById('checkboxAddress').onchange = function () {
    profileApp.validator.checkAddress();
};


