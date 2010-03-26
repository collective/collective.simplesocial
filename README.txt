Introduction
============

collective.simplesocial exposes some basic features of Facebook's "Facebook
Connect" API for use within Plone.

The goals of this Plone add-on product are to:
 * Provide the basic infrastructure required as a foundation for custom
   Facebook API integrations. (e.g. API key configuration, inclusion of needed
   code snippets)
 * Expose selected high-value prepackaged components of Facebook's API without
   requiring deep knowledge of the inner workings of the API.

Current features include:
 * Basic Facebook Connect integration
 * Fan Box portlet
 * Feed Form portlet
 * Post to Facebook Fan Page

(Each feature appears separately in the quick installer and Add/Remove Products
configlet.)

To see a demonstration of the feed form portlet in use, watch the `screencast`_.

.. _`screencast`: http://screencast.com/t/jiMl7nQrN

Compatibility
=============

collective.simplesocial has been tested with Plone 3.x and Plone 4.0.

It has been tested with Firefox 3.5, Safari 4, and IE 6, 7, and 8.


Fan Box Portlet
===============

Facebook provides a basic "`Fan Box`_" widget which can be used to promote
a Facebook Page by prompting visitors to your website to become a fan and
allowing them to view the Page's activity stream and fans.

.. _`Fan Box`: http://wiki.developers.facebook.com/index.php/Fan_Box

collective.simplesocial allows insertion of a Fan Box as a portlet.

Prerequisites
-------------

This product loads the Fan Box within an iframe, so it does not require a
Facebook API key or creating a Facebook application.  You must already have
created a Facebook Page, however.  Take note of the numeric ID of the Page
(it appears in the URL when viewing the page in Facebook).

Adding a Fan Box
----------------

1. Go to Site Setup.
2. Click Add/Remove Products.
3. Check 'Facebook Fan Box portlet' and click Install.
4. Navigate to the location in the site where you want to add the portlet.
5. Click 'Manage portlets'.
6. Click on the dropdown to add a portlet to the column where you want
   the fan box to appear, and select 'Facebook Fan Box'.
7. Paste in the numeric ID of the Facebook Page you want to promote.
8. You may configure whether or not an activity stream appears, the number of
   fan connections to display, and the width and height of the fan box.
9. Click save and return to the location where you assigned the portlet to
   view the fan box.


Feed Form Portlet
=================

Facebook allows Facebook Connect sites to publish messages to users' activity
streams via the `Open Stream API`_ -- in particular, via the
`FB.Connect.streamPublish`_ method.

.. _`Open Stream API`: http://wiki.developers.facebook.com/index.php/Using_the_Open_Stream_API
.. _`FB.Connect.streamPublish`: http://wiki.developers.facebook.com/index.php/FB.Connect.streamPublish

collective.simplesocial provides a "Feed Form" portlet. This allows you to
configure a dialog which will pop up on page load and prompt the user to post
a message to his or her Facebook feed.  This can be used to prompt a visitor to
your Plone site to publicize some action that they took on the site.  For
example, you could add this portlet to the thank you page of a PloneFormGen
form, asking the user to tell his or her friends about the site.

Since it makes use of the full Facebook Connect API, using the feed form portlet
requires first setting up a Facebook Application and setting its API Key in the
Facebook Connect control panel in Plone's site setup.

Creating a Facebook Application
-------------------------------

1. Go to the `Facebook Developer application`_. If prompted, allow it access to
   your profile.
2. Click the `Set Up New Application` button and fill out the form.
3. Take note of the `API Key` that is displayed.
4. In the Facebook application's settings, click on the `Connect` tab.
   Enter the URL of the site into the `Connect URL` field.  *Note:
   This site must be publicly accessible in order for communication between Facebook
   and the site to work.*

.. _`Facebook Developer application`: http://www.facebook.com/developers/

Adding a Feed Form
------------------

1. Go to Site Setup.
2. Click `Add/Remove Products`.
3. Check 'Facebook Feed Form portlet' and click Install.
4. Return to Site Setup.
5. Click `Facebook Connect`.
6. Paste in the API Key that you recorded above when creating your Facebook
   application.  Click Save.  If successful, you should see a yellow message
   saying that the connection has been verified.
7. Navigate to the location in the site where you want to add the portlet.
8. Click 'Manage portlets'.
9. Click on the dropdown to add a portlet to the column where you want
   the feed form to appear, and select 'Facebook Feed Form'.
10. Edit the settings as prompted.  When finished, click Save.
11. Return to the location where you assigned the portlet to view the feed
    form.

If a visitor to a page with a feed form is not logged into Facebook, then the
feed form will not appear automatically.  Instead, a message will be shown
along with a Facebook Connect button.  Clicking this button will allow the
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
documentation for the `FB.Connect.streamPublish`_ method and `Attachment`_
object.

.. _`FB.Connect.streamPublish`: http://wiki.developers.facebook.com/index.php/FB.Connect.streamPublish
.. _`Attachment`: http://wiki.developers.facebook.com/index.php/Attachment_%28Streams%29

Post to Facebook Fan Page
=========================

This feature adds a "Post to Fan Page" link to the document actions area of a
Plone page.  The link only shows up for Managers.

Since it makes use of the full Facebook Connect API, using this feature requires
first setting up a Facebook Application and setting its API Key in the
Facebook Connect control panel in Plone's site setup.  The ID of the fan page
you want to post to must also be entered there.

The string "utm_source=facebook" will be added to the page URL, so that visitors
who arrive at your site via the posted link can be tracked in Google Analytics.


Configuring the 'Post to Fan Page' feature
------------------------------------------

1. Follow the instructions above for creating a Facebook Application.
2. Go to Site Setup.
3. Click `Add/Remove Products`.
4. Check 'Post to Facebook Fan Page' and click Install.
5. Return to Site Setup.
6. Click `Facebook Connect`.
7. Paste in the API Key that you recorded above when creating your Facebook
   application.  Click Save.  If successful, you should see a yellow message
   saying that the connection has been verified.
8. Select the Facebook fan page you want to post to.

Now the 'Post to Fan Page' link should show up when you are logged in. To post
to Facebook, click on the link.  You will be prompted to confirm the message
that will be posted.


Custom Facebook Connect Integration
===================================

This product provides the basic pieces needed to integrate with Facebook using
custom `XFBML`_ and/or the `Facebook Javascript API`_.  It is possible to
install these basic components without installing either of the above two
portlets, by selecting and installing `Basic Facebook Connect Integration`
from the Add/Remove Products configlet.

This will install:
 * The Facebook Connect configlet for configuring your API key.
 * A browser resource called xd_receiver.htm for facilitating cross-domain
   communication with Facebook.
 * A "feature loader" viewlet in the portaltop viewlet manager, which loads
   the Facebook Connect javascript and initializes Facebook Connect with
   the configured API key.

With these pieces in place and a correct API key, you should be able to use
XFBML and the Facebook Javascript API wherever you like in Plone templates.

Miscellaneous tips
------------------

* The TAL parser likes to complain about mismatched tags when using tags with
  the 'fb' XML namespace.  You may need to escape such tags and include them
  with a tal:replace (see configlet.pt in this package for an example).  Or
  put them in a separate file and include them via a browser view method that
  reads that file.

* Use the FB.ensureInit method to wrap code that should not run until the
  Facebook components (which load in a deferred fashion) have completed
  loading.  For example, the following will alert the UID of the logged-in
  Facebook user once initialization is complete::

    FB.ensureInit(function() {
      alert(FB.Connect.get_loggedInUser());
    });

* Use logic like the following to do something different depending on whether
  or not the user is already logged into Facebook::
  
    var fb_status = FB.Connect.get_status().result;
    if (fb_status == FB.ConnectState.connected ||
        fb_status == FB.ConnectState.appNotAuthorized) {
        // -- action if logged in --
    } else {
        // -- action if logged out --
    }

Additional Facebook Connect API Resources
-----------------------------------------

 * `Facebook Developer Wiki`_
 * `Facebook Connect documentation`_
 * `Facebook Javascript API`_
 * `XFBML`_
 
.. _`Facebook Developer Wiki`: http://wiki.developers.facebook.com/index.php/Main_Page
.. _`Facebook Connect documentation`: http://wiki.developers.facebook.com/index.php/Facebook_Connect
.. _`Facebook Javascript API`: http://wiki.developers.facebook.com/index.php/JS_API_Index
.. _`XFBML`: http://wiki.developers.facebook.com/index.php/XFBML

Credits
=======

collective.simplesocial was developed by David Glick for `Groundwire`_
(formerly ONE/Northwest).  Matt Yoder has also contributed.

.. _`Groundwire`: http://groundwire.org
