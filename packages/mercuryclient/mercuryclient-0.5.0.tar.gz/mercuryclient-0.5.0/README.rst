===========
Mercury SDK
===========

Mercury SDK can be used in projects that interface with the mercury service
that provides common internal functionality.

Initializing the client
-------------------------------
>>> from mercuryclient import MercuryApi
#Setup connection parameters
>>> conn_params = {'username': 'mercury_username', 'password':'password', 'url':'https://mercury-url.com'}
>>> m = MercuryApi(conn_params)
>>>m.send_mail(['recipent@email.com'],'Test mail', 'Mail body','ses','ses_profile')

Available APIs:
----------------------
- send_mail
- send_sms
- request_experian_report
- get_experian_response
- fetch_experian_report

Testing:
-------------
Tests are run under *tox*

You can install tox with

*pip install tox*

If using pyenv - you can do the following steps before running tox
(patch version will depend on your installations - tox only considers the major version)

>>> pyenv local 2.7.6 3.7.3 3.6.8 3.8.1

Without this step - tox will not be able to find the interpreters

Run tests using the following command

>>> tox
