from __future__ import unicode_literals

# taggit tagging APIs
from taggit.managers import TaggableManager

# import six for Python 2 and 3 compatibility.
import six

# django imports
from django.db import models
import django.utils.encoding

# django_config
from django_config.models import Config_Property

# python_utilities
#from python_utilities.logging.logging_helper import LoggingHelper
#from python_utilities.status.status_container import StatusContainer

# Message model
class Message( models.Model ):
    
    #---------------------------------------------------------------------------
    # Constants-ish
    #---------------------------------------------------------------------------

    # status values
    STATUS_NEW = "new"
    STATUS_WARNING = "warning"
    STATUS_ERROR = "error"
    STATUS_DEFAULT = STATUS_NEW
    
    STATUS_CHOICES = (
        ( STATUS_NEW, "New" ),
        ( STATUS_WARNING, "Warning" ),
        ( STATUS_ERROR, "Error" )
    )
    
    # applications
    APPLICATION_CORE = Config_Property.APPLICATION_CORE
    APPLICATION_DEFAULT = Config_Property.APPLICATION_DEFAULT
    
    #---------------------------------------------------------------------------
    # django model fields
    #---------------------------------------------------------------------------

    message = models.TextField()
    message_type = models.CharField( max_length = 255, blank = True, null = True )
    application = models.CharField( max_length = 255, blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    #status = models.CharField( max_length = 255, blank = True, null = True, choices = STATUS_CHOICES, default = STATUS_DEFAULT )
    status = models.CharField( max_length = 255, blank = True, null = True )
    tags = TaggableManager( blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'label' ]

    #----------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------


    @classmethod
    def create_message( cls, 
                        message_IN,
                        message_type_IN = None,
                        application_IN = APPLICATION_DEFAULT,
                        label_IN = None,
                        tag_list_IN = None,
                        status_IN = STATUS_DEFAULT,
                        *args,
                        **kwargs ):
                            
        '''
        Accepts all the stuff you can add to a message.  Requires message text
            and application.  Other parts are optional.  If message and
            application populated, creates message, sets properties according to
            items passed in.  On success, commits message to database and
            returns reference to message.  If error, returns None.
        '''
        
        # return reference
        message_OUT = None
        
        # declare variables.
        me = "create_message"
        new_message = None
        tag_to_apply = None
        
        # got message?
        if ( ( message_IN is not None ) and ( message_IN != "" ) ):
        
            # got message. Create Message.
            new_message = cls()
            
            # set message in instance.
            new_message.message = message_IN
            
            # got a message_type?
            if ( ( message_type_IN is not None ) and ( message_type_IN != "" ) ):
                
                # yes. Store it.
                new_message.message_type = message_type_IN
                
            #-- END check to see if message type. --#

            # got an application?
            if ( ( application_IN is not None ) and ( application_IN != "" ) ):
            
                # yes. Store it.
                new_message.application = application_IN
                
            #-- END check to see if application. --#
            
            # got a label?
            if ( ( label_IN is not None ) and ( label_IN != "" ) ):

                # yes.  Set it.
                new_message.label = label_IN

            #-- END check to see if label --#
            
            # got a status?
            if ( ( status_IN is not None ) and ( status_IN != "" ) ):

                # yes.  Set it.
                new_message.status = status_IN

            #-- END check to see if status --#
            
            # save message, so it exists to append tags to.
            new_message.save()
            
            # got a list of one or more tags?
            if ( ( tag_list_IN is not None ) and ( isinstance( tag_list_IN, list ) == True ) and ( len( tag_list_IN ) > 0 ) ):

                # yes.  Loop over tags list.
                for tag_to_apply in tag_list_IN:
                
                    # tag the message with each tag in the list.
                    new_message.tags.add( tag_to_apply )
                    
                #-- END loop over tag list. --#

            #-- END check to see if tag list passed in. --#
            
            # place message in return reference.
            message_OUT = new_message

        else:
        
            # no message, which is required.
            message_OUT = None
            
        #-- END check to see if message text --#
        
        return message_OUT
    
    #-- END class method create_message() --#


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------

    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # got ID?
        if ( self.id ):
        
            string_OUT = str( self.id ) + " - "
            
        #-- END check to see if ID present (proxy for "If in database").
        
        # application
        if ( ( self.application is not None ) and ( self.application != "" ) ):

            # yes.  Output application.
            string_OUT += " - Application: " + self.application

        #-- END check to see if application. --#
        
        # message
        if ( ( self.message is not None ) and ( self.message != "" ) ):
        
            # yes.  Output message.
            string_OUT += " - Message: " + self.message
        
        #-- END check to see if message present. --#
        
        return string_OUT

#= End Message Model =========================================================
