class ZivverMissingRequiredFields(Exception):
    """When there are missing required fields missing"""
    pass


class ZivverCRUDError(Exception):
    """When there are erros in the response"""

    def __init__(self, message, response, code=None, params=None):
        """
        Exception raised only when there are CRUD errors from Zivver.
        Saves the response object inside the response variable
        """
        super().__init__(message, code, params)

        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason
        self.text = response.text

    def get_error_message(self):
        """
        :return: formatted text error message
        """
        return 'Status code: {}, Reason: {}, Text: {}'.format(self.status_code, self.reason, self.text)

    def get_sollution(self):
        """
        Error messages come from Zivver:
        https://docs.zivver.com/en/admin/synctool/troubleshooting/synchronization-log-errors.html
        :return: Sollutions based on Zivver cause
        """
        if 'Error creating alias: Alias is already taken for' in self.text:
            return """
                Cause
                The message Alias is already taken means that the email alias is a separate 
                account on the Zivver platform, instead of being an email alias like in Exchange.
                
                Solution
                To keep the received Zivver messages accessible to the recipient, 
                email alias must be manually merged on our platform to the primary email address.
                
                On the Account page, find the Zivver account that is mentioned first in the 
                error and merge the account mentioned after "error creating alias: 
                Alias is already taken for "ZivverUID" in the error.
                How to merge two accounts\r\n"""
        if 'Unknown account with uuid:' in self.text:
            return """
                Account probably does not exist, did you create the account?\r\n"""
        if 'Account is outside the organization' == self.text:
            return """
                There are multiple possible causes for this error:
                
                Cause 1
                The email address mentioned exists outside your Zivver organization. If this is the case, then you will
                not find the account on the Account page when you search for the email address. If you do find the 
                account, then go to Cause 2 below.

                Solution
                Go the the Domain page.
                Adopt free accounts

                Cause 2
                The Synctool tries to convert a Zivver user account to a functional account or the other way around. 
                The Synctool can’t change account types.
                
                Solution
                Change the account type of the account. Use the table below for the recommended 
                Zivver account types for each type of mailbox.
                
                Mailbox type	    Recommended Zivver account type
                User mailbox        Normal account
                Shared mailbox      Functional account\r\n"""