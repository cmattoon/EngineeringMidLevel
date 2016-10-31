/**
 * This is the code for the main UI VM. Ideally, this
 * would be in a directory like 'assets/js/Models/' 
 * or something and loaded via Require.js. The JS can
 * load asynchronously, which drastically cuts the 
 * time-to-first-byte. It's a pain to get it working
 * nicely with all of the other libraries.
 */

/**
 * DatePicker Binding 
 * From: http://stackoverflow.com/questions/18016718/using-knockout-js-how-do-bind-a-date-property-to-a-html5-date-pickerx
 */
ko.bindingHandlers.datePicker = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {                    
        // Register change callbacks to update the model
        // if the control changes.       
        ko.utils.registerEventHandler(element, "change", function () {            
            var value = valueAccessor();
	    var date = new Date(element.value);
	    var date_string = [
		date.getFullYear(),
		date.getMonth()+1, // Zero-indexed months
		date.getDate()
	    ].join('-');

	    value(date_string);
        });
    },
    // Update the control whenever the view model changes
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var value =  valueAccessor();        
        element.value = value();
    }
};


function _ajax(url, method, data) {
    var request = {
	url: url,
	type: method || 'GET',
	cache: false,
	dataType: 'json',
	contentType: 'application/json',
	accepts: 'application/json',
	/*
	  beforeSend: function(xhr) {
	  xhr.setRequestHeader("Auth goes here");
	  }
	*/
	error: function(xhr) {
	    console.warn = console.warn || console.log;
	    console.warn("Ajax Error: " + xhr.status);
	}
    };
    
    if (typeof(data) !== 'undefined') {
	request.data = JSON.stringify(data);
    }
    
    return $.ajax(request);
}

function TasksViewModel() {
    var self = this;
    self.tasks = ko.observableArray();
    self.init = function() {
	self.getAllRequests();
    }
    
    
    self.getAllRequests = function() {
	_ajax('/api/features').done(function(data) {
	    for (var i = 0; i < data.length; i++) {
		self.tasks.push({
		    client: ko.observable(data[i].client),
		    title: ko.observable(data[i].title),
		    description: ko.observable(data[i].description),
		    uri: ko.observable(data[i].ticket_url),
		    
		    done: ko.observable(false)
		});
	    }
	});
    };

    self.beginAdd = function() {
	// Show dialog
	$('#dgAdd').modal('show');
    }

    /**
     * Called by DialogEditFeatureViewModel when
     * the 'Save' button is clicked.
     *
     * req object A JSON object with FeatureRequest fields
     */
    self.add = function(req) {
	console.info(req);
	return;
	_ajax('/api/feature', 'POST', req)
	    .done(function(data) {
		if (data) {
		    self.tasks.push({
			client: ko.observable(data.client),
			title: ko.observable(data.title),
			description: ko.observable(data.description),
			uri: ko.observable(data.ticket_url),
			done: ko.observable(false)
		    });
		}
	    });
    };

    self.beginEdit = function(task) {
        alert("Edit: " + task.title());
    }
    self.remove = function(task) {
        alert("Remove: " + task.title());
    }
    self.markInProgress = function(task) {
        task.done(false);
    }
    self.markDone = function(task) {
        task.done(true);
    }


}

/** For KO.observableArray */
var Client = function(id, name) {
    this.id = id;
    this.name = name;
};

/**
 * For the modal dialog
 */
function DialogFeatureEditViewModel() { 
    var self = this;
    self.title = ko.observable();
    self.description = ko.observable();
    self.clients = ko.observableArray();
    self.selectedClient = ko.observable();
    self.ticketUrl = ko.observable();
    self.targetDate = ko.observable(new Date());

    self.init = function() {
	self._getClientList();
    };

    /**
     * Queries the API for a list of clients.
     */
    self._getClientList = function() {
	_ajax('/api/clients').done(function(data) {
	    for (var i = 0; i < data.length; i++) {
		var obj = JSON.parse(data[i]);
		self.clients.push(obj);
	    }
	});
    };

    self._reset = function() {
	self.title('');
	self.description('');
    };
    
    self.saveFeature = function() {

	var request = {
	    title: self.title(),
	    description: self.description(),
	    client: self.selectedClient(),
	    ticketUrl: self.ticketUrl(),
	    targetDate: self.targetDate()
	};

	if (self.validate(request)) {
	    $('#dgAdd').modal('hide');
	    vm.add(request);
	}

	self._reset();
    };

   /**
     * Validation routine
     */
    self.validate = function(data) {
	return true;
    };
}
