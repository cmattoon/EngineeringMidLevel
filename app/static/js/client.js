/**
 * This is the code for the main UI VM. Ideally, this
 * would be in a directory like 'assets/js/Models/' 
 * or something and loaded via Require.js. The JS can
 * load asynchronously, which drastically cuts the 
 * time-to-first-byte. It's a pain to get it working
 * nicely with all of the other libraries.
 */
function TasksViewModel() {
    var self = this;
    self.tasks = ko.observableArray();
    self.init = function() {
	self.getAllRequests();
    }
    
    self.ajax = function(url, method, data) {
	var request = {
	    url: url,
	    type: method || 'GET',
	    cache: false,
	    dataType: 'json',
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
    };
    
    self.getAllRequests = function() {
	self.ajax('/api/features').done(function(data) {
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
        alert("Add");
    }
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
//vm = new TasksViewModel();
//vm.init();

//ko.applyBindings(vm, $('#main')[0]);