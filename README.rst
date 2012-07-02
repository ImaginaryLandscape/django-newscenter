==========
Newscenter
==========

A Django application for creating news releases which can be associated with unique newsroom objects.

A Django CMS apphook is included as well as a templatetag for rendering news release headlines in non-application templates.

Installation
============

#. Add newscenter to your python path
#. Add the following to the INSTALLED_APPS of your project's settings.py::
	'newscenter',
#. In your urls.py, add
	(r'^news/', include('newscenter.urls')),
#. Run::
	manage.py syncdb
	manage.py collectstatic
#. Load the initial newsroom object from the newscenter fixtures directory:
	manage.py loaddata newscenter/fixtures/newsroom.json. 
   This has not been called initial_data.json because we want it to be editable and not reset every time syncdb is run.
