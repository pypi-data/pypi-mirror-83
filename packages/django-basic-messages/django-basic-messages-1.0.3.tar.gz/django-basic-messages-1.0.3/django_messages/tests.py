"""
This file contains tests of the Message model.
"""

# django imports
import django.test

# django_messages imports
from django_messages.models import Message


class MessageModelTest( django.test.TestCase ):
    
    #----------------------------------------------------------------------------
    # Constants-ish
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def setUp( self ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """

        # call TestHelper.standardSetUp()
        pass

    #-- END function setUp() --#
        

    def test_create_message( self ):
        
        # declare variables
        me = "test_create_message"
        application = ""
        message = ""
        message_type = None
        label = ""
        status = ""
        tag_list = []
        message_instance = None
        test_application = ""
        test_message = ""
        test_message_type = ""
        test_label = ""
        test_status = ""
        test_tag_list = []
        test_tag_qs = None
        test_tag_count = -1
        what_is_it = ""
        test_value = ""
        should_be = -1
        do_strict = False
        do_partial = False
        error_string = ""
        test_qs = None
        match_count = -1
        message_qs = None
        message_count = -1
        
        #----------------------------------------------------------------------#
        # Defaults
        #----------------------------------------------------------------------#

        # set up message values
        message = "test message"
        
        # make instance
        message_instance = Message.create_message( message )
        
        # make sure there are values for everything.
        
        # application
        what_is_it = "application"
        test_application = message_instance.application
        test_value = test_application
        should_be = Message.APPLICATION_DEFAULT
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message type
        what_is_it = "message_type"
        test_message_type = message_instance.message_type
        test_value = test_message_type
        should_be = None
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message
        what_is_it = "message"
        test_message = message_instance.message
        test_value = test_message
        should_be = message
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # label
        what_is_it = "label"
        test_label = message_instance.label
        test_value = test_label
        should_be = None
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # status
        what_is_it = "status"
        test_status = message_instance.status
        test_value = test_status
        should_be = Message.STATUS_DEFAULT
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # should be no tags.
        what_is_it = "tag count"
        test_tag_qs = message_instance.tags.all()
        test_tag_count = test_tag_qs.count()
        test_value = test_tag_count
        should_be = 0
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # Values set
        #----------------------------------------------------------------------#

        # set up message values
        application = "unit_test"
        message = "test message"
        message_type = "test message type"
        label = "test"
        status = Message.STATUS_NEW
        tag_list = [ "awesome", "test" ]
        
        # create instance
        # make instance
        message_instance = Message.create_message( message,
                                                   message_type_IN = message_type,
                                                   application_IN = application,
                                                   label_IN = label,
                                                   tag_list_IN = tag_list,
                                                   status_IN = status )
        
        # make sure there are values for everything.
        
        # application
        what_is_it = "application"
        test_application = message_instance.application
        test_value = test_application
        should_be = application
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message
        what_is_it = "message"
        test_message = message_instance.message
        test_value = test_message
        should_be = message
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message type
        what_is_it = "message_type"
        test_message_type = message_instance.message_type
        test_value = test_message_type
        should_be = message_type
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # label
        what_is_it = "label"
        test_label = message_instance.label
        test_value = test_label
        should_be = label
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # status
        what_is_it = "status"
        test_status = message_instance.status
        test_value = test_status
        should_be = status
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # should be no tags.
        what_is_it = "tag count"
        test_tag_qs = message_instance.tags.all()
        test_tag_count = test_tag_qs.count()
        test_value = test_tag_count
        should_be = 2
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # try database lookups.
        #----------------------------------------------------------------------#
        
        # get all messages
        message_qs = Message.objects.all()
        
        # how many?
        what_is_it = "message count"
        message_count = message_qs.count()
        test_value = message_count
        should_be = 2
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # set up message values
        application = "unit_test"
        message = "test message"
        label = "test"
        status = Message.STATUS_NEW
        tag_list = [ "awesome", "test" ]
        
        # get message for application = "unit_test"
        message_qs = message_qs.filter( application = application )
        message_instance = message_qs.get()

        # application
        what_is_it = "application"
        test_application = message_instance.application
        test_value = test_application
        should_be = application
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message
        what_is_it = "message"
        test_message = message_instance.message
        test_value = test_message
        should_be = message
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # message type
        what_is_it = "message_type"
        test_message_type = message_instance.message_type
        test_value = test_message_type
        should_be = message_type
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # label
        what_is_it = "label"
        test_label = message_instance.label
        test_value = test_label
        should_be = label
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # status
        what_is_it = "status"
        test_status = message_instance.status
        test_value = test_status
        should_be = status
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

        # should be 2 tags.
        what_is_it = "tag count"
        test_tag_qs = message_instance.tags.all()
        test_tag_count = test_tag_qs.count()
        test_value = test_tag_count
        should_be = 2
        error_string = "Found " + what_is_it + " \"" + str( test_value ) + "\", should be \"" + str( should_be ) + "\""
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_create_message() --#


#-- END test class MessageModelTest --#
