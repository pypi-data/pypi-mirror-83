socialoauth plugin for `Grvlms <https://docs.grvlms.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/groovetch/grvlms-socialoauth

Usage
-----

::

    grvlms plugins enable socialoauth

Configuration
-------------

::
    grvlms socialoauth config -i (Run interactively to config ID azure client and secret key)
    grvlms socialoauth config -s (Set a configuration value base on format KEY=VAL)

Azure Configuration
-------------------

::
    - We must to set `SOCIALOAUTH_AZURE_CLIENT_ID` and `SOCIALOAUTH_AZURE_SECRET_KEY` variable. (Get them in your azure-portal).
      (If you don't have Azure portal account yet, please register at https://azure.microsoft.com/en-us/features/azure-portal)
    - Authorized redirect URIs at Azure portal: `https://{site_name}/auth/complete/google-oauth2/`
        (more infomation at https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/)
    - Make sure `SOCIALOAUTH_ACTIVATE_AZURE` is true.
    - Set ENABLE_AZURE_PICTURE_PROFILE: true if you want to enable edx-azuresso app

Google Configuration
--------------------

::
    - We must to set `SOCIALOAUTH_GOOGLE_CLIENT_ID` and `SOCIALOAUTH_GOOGLE_SECRET_KEY` variable. (Get them in Google API Console).
      (If you don't have account yet, please register at https://console.developers.google.com)
    - Authorized redirect URIs at Google API Console: `https://{site_name}/auth/complete/google-oauth2/`
        (more infomation at https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/)
    - Make sure `SOCIALOAUTH_ACTIVATE_GOOGLE` is true.
    - Set ENABLE_GOOGLE_PICTURE_PROFILE: true if you want to enable edx-googlesso app

Finally
-------
::
    - grvlms images build openedx (update Dockerfile)
    - grvlms local start (If you run on Local ENV)
    - grvlms socialoauth init (run migration to update Provider Configuration records)
    

License
-------

This software is licensed under the terms of the AGPLv3.
