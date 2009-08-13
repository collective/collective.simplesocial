FB.ensureInit(function() {
  var default_tpl = {
    'one_line_story_templates': ['{*actor*} {*msg*}'],
    'short_story_templates': [{'template_title': '', 'template_body': '{*actor*} {*msg*}'}],
    'action_links': [{'text': '{*actiontext*}', 'href': '{*actionhref*}'}]
    }

  var recursive_compare = function(o1, o2) {
    for(p in o1) {
      switch(typeof(o1[p])) {
        case 'object':
          if (!recursive_compare(o1[p], o2[p])) { return false }; break;
        case 'function':
          if (typeof(o2[p])=='undefined' || (o1[p].toString() != o2[p].toString())) { return false; }; break;
        default:
          if (o1[p] != o2[p]) { return false; }
      }
    }
    for(p in o2) {
      if(typeof(o1[p])=='undefined') {return false;}
    }
    return true;
  }

  var find_or_create_template_bundle = function(tpls) {
    var tpl_id = null;
    for (i = 0; i<tpls.length; i++) {
        tpl = tpls[i];
        var tmp_tpl_id = tpl.template_bundle_id;
        // delete to facilitate comparison
        delete tpl['template_bundle_id'];
        delete tpl['time_created'];
        if (recursive_compare(tpl, default_tpl))
          tpl_id = tmp_tpl_id;
          break;
    }
    if (tpl_id == null) {
        FB.Facebook.apiClient.callMethod('feed_registerTemplateBundle',
            {'one_line_story_templates' : '["{*actor*} {*msg*}"]',
             'short_story_templates' : '[{"template_title": "", "template_body": "{*actor*} {*msg*}"}]',
             'full_story_template': null,
             'action_links' : '[{"text": "{*actiontext*}", "href": "{*actionhref*}"}]'},
            function(result) { complete_template_bundle_registration(eval(result)); });
    } else {
        complete_template_bundle_registration(tpl_id);
    }̄
  }
  
  var complete_template_bundle_registration = function(tpl_id) {
      jq('input[id=form.template_bundle_id]').val(tpl_id);
      jq('#formfield-form-template_bundle_id').hide();
  }
  
  FB.Connect.requireSession(function() {
    FB.Facebook.apiClient.callMethod('feed_getRegisteredTemplateBundles',
      {}, function(result) { find_or_create_template_bundle(eval(result)) });
  });

  jq('input[type=text]').attr('size', '50');
});