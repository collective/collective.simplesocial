// Define the fb XML namespace for browsers that care (IE8).
document.documentElement.setAttribute('xmlns:fb', 'http://www.facebook.com/2008/fbml');
if (document.namespaces) {
  document.namespaces.add('fb');
}

var SimpleSocial = {
    callbacks: {},
    connected: false,
    settings: {},
    queue: [],
    addSettings: function (settings) {
        for (setting in settings) {
            this.settings[setting] = settings[setting];
        }
    },
    connect: function (callback) {
        // connect attempts to initialize a connection to Facebook.
        // settings.api_key must be set before this method is called.
        var app_id = parseInt(this.settings.app_id);
        var callback = this.getCallback(callback);
        if (!isNaN(app_id)) {
            var query_template = 'SELECT display_name FROM application WHERE app_id={0}';
            var apps = FB.Data.query(query_template, app_id);
            var simplesocial = this;
            FB.Data.waitOn([apps], function(args) {
                if (apps.value.length) {
                    FB.init({appId: app_id, status: true, cookie: true, xfbml: true});
                    simplesocial.connected = true;
                    callback({'connected': true, 'display_name': apps.value[0].display_name});
                } else {
                    simplesocial.connected = false;
                    callback({'connected': false});
                }
            });
        }
    },
    processQueue: function () {
        // processQueue gets called once the Facebook javascript has loaded.
        // It executes all of the functions in the queue and then replaces
        // the queue list with an object that executes functions pushed to
        // it immediately.
        for (i=0;i<this.queue.length;i++) {
            this.queue[i]();
        }
        this.queue = {
            processed: true,
            push: function (callback) {
                callback();
            }
        }
    },
    populateChoices: function (el, query) {
        // populateChoices replaces a text input with a dropdown
        // list of choices from Facebook. The list of choices comes from a
        // FB.query that includes two rows: the key and the value.
        if (el) {
            FB.Data.waitOn([query], function(args) {
                if (query.value.length && query.fields.length == 2) {
                    var choices = document.createElement('select');
                    choices.id = el.id;
                    choices.name = el.name;
                    var current_value = el.value;
                    for (i=0; i<query.value.length; i++) {
                        var row = query.value[i];
                        var option = document.createElement('option');
                        option.value = row[query.fields[0]];
                        option.text = row[query.fields[1]];
                        if (row[query.fields[0]] == current_value) option.selected = 'selected';
                        try {
                            choices.add(option, null);
                        } catch(ex) {
                            choices.add(option);
                        }
                    }
                    el.parentNode.replaceChild(choices, el);
                }
            });
        }
    },
    unpopulateChoices: function (el) {
        // Undo the changes made by populateChoices (i.e. make this field
        // back into a text input).
        if (el && el.tagName == 'SELECT') {
            var input = document.createElement('input');
            input.id = el.id;
            input.name = el.name;
            input.value = el.childNodes[el.selectedIndex].value;
            el.parentNode.replaceChild(input, el);
        }
    },
    publishToPage: function (attachment) {
        // Publishes an update to the fan page set the settings.
        FB.ui({
                method: 'stream.publish',
                attachment: attachment,
                actor_id: this.settings.page_id
            },
            this.getCallback('publishToPage')
        );
    },
    getCallback: function (callback) {
        // Gets a callback function from the callback object by name. If no
        // such function exists, it returns a null function.
        if (typeof(callback) == 'string') {
            if (this.callbacks[callback]) {
                return this.callbacks[callback];
            } else {
                return function () {};
            }
        } else if (callback == undefined) {
            return function () {};
        }
        // If the callback is not a string, we assume it is the function itself.
        return callback;
    }
};