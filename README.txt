Introduction
============

collective.simplesocial exposes some basic features of Facebook's
API for use within Plone.

The goals of this Plone add-on product are to:

* Provide the basic infrastructure required as a foundation for custom
  Facebook API integrations. (e.g. application ID configuration, inclusion
  of needed code snippets)
* Expose selected high-value prepackaged components of Facebook's API without
  requiring deep knowledge of the inner workings of the API.

Current features include:

* `Like Button`_
* `Like Box Portlet`_
* `Feed Form Portlet`_
* `Post to Facebook Fan Page`_
* `Custom Facebook Connect Integration`_

Compatibility
=============

collective.simplesocial has been tested with Plone 3.x and Plone 4.0.

It has been tested with Firefox 3.5, Safari 4, and Internet Explorer 7 and 8.
Internet Explorer 6 is no longer supported.

Creating a Facebook Application
===============================

Before you can use the features of collective.simplesocial, you need to create
a Facebook application. To do so, follow these steps:

1. Go to the `Facebook Developer application`_. If prompted, allow it access to
   your profile.
2. Click the `Set Up New Application` button and fill out the form.
3. Take note of the `Application ID` that is displayed.
4. In the Facebook application's settings, click on the `Connect` tab.
   Enter the URL of the site into the `Connect URL` field.
5. Return to your Plone site, and enter the Facebook application ID in the
   Facebook Settings control panel. Then use the provided button to log into
   Facebook and connect with your Facebook application.
   
.. _`Facebook Developer application`: http://www.facebook.com/developers/

Like Button
===========

A Facebook `Like button`_ allows visitors to establish a lasting connection
between their Facebook profile and a piece of content on your site.

.. _`Like button`: http://developers.facebook.com/docs/reference/plugins/like

Prerequisites
-------------

To add Like buttons to your site, first follow the instructions for `Creating a
Facebook Application`_ above.

Adding Like Buttons
-------------------

1. Go to Site Setup.
2. Click Facebook Settings.
3. Log into Facebook using the provided button if you have not done so already.
4. On the Like Button tab, make sure that "Display Like buttons on this site"
   is checked.
5. Choose the content types where you want Like buttons to appear by default.
6. Set the display options for your Like buttons.
7. Save your settings.

Enabling and Disabling Like Buttons
-----------------------------------

In addition to choosing the content types where Like buttons will be displayed,
you can also turn the Like button on or off for a particular piece of content.
To do so, browse to the content item, and select "Show Like Button" or "Hide
Like Button" from the Actions menu.

Customizing Open Graph Metadata
-------------------------------

To find out about the piece of content that is being liked, Facebook reads
metadata from Open Graph tags in the head of the page. By default, Simple
Social provides metadata based on these fields:

* The title of the content item
* The URL of the content item
* The content item's description, if it provides one
* The content item's preview image, if it provides one, or the site logo
* The site name
* The Facebook application ID

All content items other than the site's home page are listed as type "article."
The site's home page is listed as type "website."

The Open Graph metadata can be customized on a per-content type basis by
registering an adapter that provides
collective.simplesocial.likebutton.interfaces.IOpenGraphProvider for the
content type's interface. In cases where more than one content type provides
the same interface, the adapter can be named to match the desired portal type.
For an example, see the default implementation in
collective.simplesocial.likebutton.opengraph.DefaultOpenGraphProvider.


Like Box Portlet
================

Facebook provides a basic `Like Box`_ widget which can be used to promote
a Facebook Page by prompting visitors to your website to like the Page and
allowing them to view the Page's activity stream and fans.
collective.simplesocial allows insertion of a Like Box as a portlet.

.. _`Like Box`: http://developers.facebook.com/docs/reference/plugins/like-box

Prerequisites
-------------

To use the Like Box portlet, you must complete the steps in the section on
`Creating a Facebook Application`_. You also need a Facebook Page.
Take note of the URL of the Page, and enter in when you create the portlet.

Adding a Like Box
-----------------

1. Navigate to the location in the site where you want to add the portlet.
2. Click 'Manage portlets'.
3. Click on the dropdown to add a portlet to the column where you want
   the like box to appear, and select 'Facebook Like Box'.
4. Paste in the URL of the Facebook Page you want to promote.
5. You may configure whether or not an activity stream appears, the number of
   fan connections to display, and the width of the like box.
6. Click save and return to the location where you assigned the portlet to
   view the Like box.


Feed Form Portlet
=================

Facebook allows sites to publish messages to users' activity streams using
the `stream.publish`_ API method.

.. _`stream.publish`: http://developers.facebook.com/docs/reference/rest/stream.publish

collective.simplesocial provides a "Feed Form" portlet. This allows you to
configure a dialog which will pop up on page load and prompt the user to post
a message to his or her Facebook feed.  This can be used to prompt a visitor to
your Plone site to publicize some action that they took on the site.  For
example, you could add this portlet to the thank you page of a PloneFormGen
form, asking the user to tell his or her friends about the site.

To see a demonstration of the feed form portlet in use, watch the `screencast`_.

.. _`screencast`: http://screencast.com/t/jiMl7nQrN

Prerequisites
-------------

To use the Feed Form portlet, you must first complete the steps in the
section on `Creating a Facebook Application`_.

Adding a Feed Form
------------------

1. Navigate to the location in the site where you want to add the portlet.
2. Click 'Manage portlets'.
3. Click on the dropdown to add a portlet to the column where you want
   the feed form to appear, and select 'Facebook Feed Form'.
4. Edit the settings as prompted.  When finished, click Save.
5. Return to the location where you assigned the portlet to view the feed
   form.

If a visitor to a page with a feed form is not logged into Facebook, then the
feed form will not appear automatically.  Instead, a message will be shown
along with a Facebook login button.  Clicking this button will allow the
visitor to log into Facebook, after which the feed form will be displayed.

Customizing the Feed Attachment
-------------------------------

When a user submits a feed form, collective.simplesocial sends along an
attachment to Facebook with information about the content item where the
feed form was displayed. By default, this attachment contains the following
information:

* The title of the content item
* The URL of the content item
* The content item's description, if it provides one
* The content item's tile image, if it provides one, or the site logo

These defaults are provided by the DefaultFeedFormDataProvider adapter. It
is possible to override the defaults globally or for a particular content type
by registering an adapter that provides the IFeedFormDataProvider interface.
This interface provides methods for getting the attachment for the current
context and for overriding the settings specified in the portlet assignment.
For more information, see 
collective.simplesocial.feedform.facebookfeedform.IFeedFormDataProvider and the
documentation for the `stream.publish`_ method and `stream attachment`_
object.

.. _`stream.publish`: http://developers.facebook.com/docs/reference/rest/stream.publish
.. _`stream attachment`: http://developers.facebook.com/docs/guides/attachments

Post to Facebook Fan Page
=========================

This feature adds a "Post to Fan Page" link to the document actions area of a
Plone page.  The link only shows up for Managers.

The string "utm_source=facebook" will be added to the page URL, so that visitors
who arrive at your site via the posted link can be tracked in Google Analytics.

Prerequisites
-------------

To use the Post to Facebook Fan Page feature, you must first complete the steps
in the section on `Creating a Facebook Application`_.

Configuring the 'Post to Fan Page' feature
------------------------------------------

1. Go to Site Setup.
2. Click Facebook Settings.
3. Log into Facebook using the provided button if you have not done so already.
4. On the Post to Page tab, make sure that "Allow site managers to post updates
   to a Facebook Page" is checked.
5. Select the Facebook page you want to post to. Click Save.

Now the 'Post to Fan Page' link should show up when you are logged in. To post
to Facebook, click on the link.  You will be prompted to confirm the message
that will be posted.


Custom Facebook Connect Integration
===================================

This product provides the basic pieces needed to integrate with Facebook using
custom `XFBML`_ and/or the `Facebook JavaScript SDK`_. These include:

* The Facebook Settings control panel for configuring your application ID.
* The SimpleSocial javascript library, which wraps some of the most common
  calls to the Facebook API and provides a standard framework for queuing
  and executing functions when the Facebook javascript library has loaded.
* A Facebook initialization viewlet in the portaltop viewlet manager, which
  connects to Facebook using the application ID provided in the Facebook
  Settings control panel.

With these pieces in place and a correct application ID, you should be
able to use XFBML wherever you like in Plone templates. You can also
make use of the Facebook Javascript API. (See the example below for
correct usage.)

Miscellaneous Tips
------------------

* The TAL parser likes to complain about mismatched tags when using tags with
  the 'fb' XML namespace.  You may need to escape such tags and include them
  with a tal:replace or put them in a separate file and include them via a
  browser view method that reads that file.

* The Facebook javascript library is loaded asynchronously, which means that
  Facebook API calls cannot be made immediately when the page is loaded.
  To address this issue, the SimpleSocial javascript library implements a
  queue that stores functions that depend on the Facebook API until the API
  is fully loaded. It then executes all of the functions in the queue in the
  order that they were inserted. Functions passed to the queue after the
  Facebook API has loaded are executed immediately.
  
  SimpleSocial.queue behaves like a javascript array. To add a function to
  the queue, use the push method::
    
    SimpleSocial.queue.push(function () {
      // Do something using the Facebook API.
    });

* Use logic like the following to do something different depending on whether
  or not the user is already logged into Facebook and connected to your
  application::
  
    SimpleSocial.queue.push(function () {
      FB.getLoginStatus(function (response) {
        if (response.session) {
          // The user is logged in and connected.
        } else {
          // The user is not logged in or is not connected
          // to your application.
        }
      });
    });
    
  For more information, see the documentation for `FB.getLoginStatus`_.
  
  .. _`FB.getLoginStatus`: http://developers.facebook.com/docs/reference/javascript/FB.getLoginStatus

Additional Facebook API Resources
---------------------------------

 * `Facebook Developer Documentation`_
 * `Facebook JavaScript SDK`_
 * `Social Plugins`_
 * `XFBML`_
 
.. _`Facebook Developer Documentation`: http://developers.facebook.com/docs/
.. _`Facebook JavaScript SDK`: http://developers.facebook.com/docs/reference/javascript/
.. _`Social Plugins`: http://developers.facebook.com/plugins
.. _`XFBML`: http://developers.facebook.com/docs/reference/javascript/FB.XFBML.parse

Credits
=======

collective.simplesocial was developed by David Glick for `Groundwire`_
(formerly ONE/Northwest).  Matt Yoder has also contributed.

.. _`Groundwire`: http://groundwire.org

Thanks to `Nouveller`_ for the Facebook icon.

.. _`Nouveller`: http://www.nouveller.com/
