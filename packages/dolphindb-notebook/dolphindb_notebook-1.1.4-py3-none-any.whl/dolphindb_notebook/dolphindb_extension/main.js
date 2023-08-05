define([
    'base/js/namespace',
	'base/js/events'
], function(Jupyter) {

    var Notebook = require('notebook/js/notebook').Notebook
	"use strict";
	var mod_name = "DolphinDB Extension";
    var log_prefix = ' [' + mod_name + '] ';

	var creds;
	var enableSSL = false;
	var kernel = Jupyter.notebook.kernel;

	var handle_output = function(out) {
		if(out.msg_type === "stream") {
			var json_text = out.content.text;
			var res = JSON.parse(json_text);
			creds = res;
		}
	};

	var sleep = function(numberMillis) {
		var now = new Date();
		var exitTime = now.getTime() + numberMillis;
		while (true) {
			now = new Date();
			if(now.getTime() > exitTime) {
				return;
			}
		}
	};

	var retrieve_creds = function() {
		// if no kernel is available: pause loading js extension until a kernel is ready
		while(typeof kernel === "undefined" || kernel === null) {
			console.log('======sleep until kernel is ready======');
			sleep(250);
			kernel = Jupyter.notebook.kernel;
		}
		// if a dolphindb kernel is available: retrieve creds info
		if(kernel.name === 'dolphindb') {
			var code_input = 'retrieve-credentials';
			var callbacks = { 'iopub' : {'output' : handle_output}};
			kernel.execute(code_input, callbacks, {silent: false});
		}
	};

	retrieve_creds();

    var getUserInput = function() {
		require([
			'jquery',
			'base/js/dialog'
		], function($, dialog) {
			// user's selection: to be determined when onchange event gets triggered later
			var idx = null; 
			var server = null;
			var port = null;
			var username = null;
			var password = null;
			// radio buttons for selection
			var selection = $('<table class="table" id="cred"/>');
			for(var item in creds) {
				var cred = creds[item];
				var option = cred['server'] + ': ' + cred['port'] + ' - ' + cred['user'];
				selection.append($('<tr><td><input name="option" type="radio" onclick="document.option_selected(this)" value=' + item + '>' + '		' + option + '</td></tr>'));
			}
			// body
			var body = $('<div/>');
			// select server
			body.append($('<h4/>').text('Select server'));
			body.append($('<p/>').html(selection));
			// onclick event on radio buttons
			document.option_selected = function(myRadio) {
				idx = myRadio.value;
				var selected = creds[idx];
				server = selected['server'];
				port = selected['port'];
				username = selected['user'];
				password = selected['password'];
			};
			// enable ssl
			var sslBox = $('<input name="ssl" type="checkbox" onclick="checkboxOnclick(this)">\
										  <label>		  Enable SSL</label>');
			// body.append($)
			body.append($('<p/>').html(sslBox));
			// onclick event on check box
			checkboxOnclick = function(checkbox) {
				if(checkbox.checked == true) {
					enableSSL = true;
				} else {
					enableSSL = false;
				}
			}
			// dialog
			dialog.modal({
				title: 'Connect to DolphinDB',
				body: body,
				buttons: {
					// use selected one from previous and connect to ddb
					'Connect': {
						class: "btn-primary",
						click: function() {
							if(idx === null) {
								alert('Please select the credential you want to use to connect to DolphinDB server :)');
							} else {
								kernel.execute('connect-to-ddb-pre ' + server + ' ' + port + ' ' + username + ' ' + password + ' ' + enableSSL);
							}
						}
					},
					// get new credential from user input
					'New': {
						class: "btn-success",
						click: function() {
							// disable keyboard shortcuts temporarily
							Jupyter.keyboard_manager.disable();
							// get user's new credential through html form in dialog
							var body = $('<div/>');
							body.append($('<h4/>').text('Please enter your new credential info'));
							body.html(
								'<form>\
								<div class="form-group">\
								<label for="server">Server: </label>\
								<input class="form-control" id="server" type="text">\
								</div>\
								<div class="form-group">\
								<label for="port">Port: </label>\
								<input class="form-control" id="port" type="text">\
								</div>\
								<div class="form-group">\
								<label for="username">Username: </label>\
								<input class="form-control" id="username" type="text">\
								</div>\
								<div class="form-group">\
								<label for="password">Password: </label>\
								<input class="form-control" id="password" type="password">\
								</div>\
								<div class="form-group">\
								<input class="form-control" id="enableSSL" type="checkbox">\
								</div>\
								</form>'
							);
							// dialog
							dialog.modal({
								title: 'Connect to DolphinDB',
								body: body,
								buttons: {
									'Save & Connect': {
										class: "btn-primary",
										click: function() {
											// use user's input to connect to DolphinDB
											var server = $("#server").val();
											var port = $("#port").val();
											var username = $("#username").val();
											var password = $("#password").val();
											var enableSSL = $("#enableSSL").checked;
											kernel.execute('connect-to-ddb-new ' + server + ' ' + port + ' ' + username + ' ' + password + ' ' + enableSSL);
										}
									},
									'Cancel': {}
								}
							});
							return true;
						}
					},
					// delete selected credential
					'Delete': {
						click: function() {
							if(idx === null) {
								alert('Please select the credential you want to delete');
							} else {
								kernel.execute('delete-cred-at ' + idx);
								alert('Completed deletion of the credential you selected :)');
							}
						}
					}
				}
			});
			return true;
		});        
	};

    var dolphinDB_button = function() {
        var action = {
            icon: 'fa-user',
            help: 'Connect to DolphinDB Server',
            help_index: 'zz',
            handler: getUserInput
        };
        var prefix = 'dolphindb_extensions';
        var action_name = 'get-user-input';
        var full_action_name = Jupyter.actions.register(action, action_name, prefix);
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    };

    var load_ipython_extension = function() {
        if(kernel.name === 'dolphindb') {
			console.log(log_prefix + 'DolphinDB kernel is available -- DolphinDB_Extension initializing ');
			// button
			dolphinDB_button();
        }
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});

