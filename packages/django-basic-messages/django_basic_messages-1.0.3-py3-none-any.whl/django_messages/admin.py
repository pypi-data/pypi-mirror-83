'''
Copyright 2013 Jonathan Morgan

This file is part of https://github.com/jonathanmorgan/django_config.

django_config is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

django_config is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with https://github.com/jonathanmorgan/django_config. If not, see http://www.gnu.org/licenses/.
'''

# import django_config class.
from django_messages.models import Message

# import django admin stuff
from django.contrib import admin

# import django db models.
from django import forms
from django.db import models

# start with default admin screens - comment out as we make fancier additions
#    below.
# admin.site.register( Message )

# get fancier

#===============================================================================
# Admin classes
#===============================================================================


#-------------------------------------------------------------------------------
# Message admin definition
#-------------------------------------------------------------------------------

class MessageAdmin( admin.ModelAdmin ):

    fieldsets = [
        ( None,
            {
                'fields' : [ 'application', 'message', 'label', 'status', 'tags' ]
            }
        ),
    ]

    list_display = ( 'last_modified', 'id', 'application', 'message', 'label' )
    list_display_links = ( 'id', 'message', )
    list_filter = [ 'application', 'label', 'status' ]
    search_fields = [ 'id', 'application', 'message', 'label', 'status' ]
    # date_hierarchy = 'status_date'
    # actions = [ toggle_published_flag ]
    ordering = [ '-last_modified' ]

#-- END MessageAdmin admin class --#

admin.site.register( Message, MessageAdmin )