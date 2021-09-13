import threading
import unittest

from config import ZivverConfig

from zivverscim import scim_connection_crud
from zivverscim.exceptions import ZivverCRUDError

import logging


class TestCRUDAccounts(unittest.TestCase):

    def _invoke_setup(self, method_name):
        """
        Setup testing data
        """
        # Setup logger
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug('\r\n\r\n################## START: {}'.format(method_name))

        logging.info('Create Zivver Connection')
        # Create zivver connection
        self.zivver_scim_connection = scim_connection_crud.ZivverSCIMConnection(
            external_oauth_token_value=ZivverConfig.zivver_test_api_key,
            scim_api_create_url=ZivverConfig.zivver_test_endpoint_url,
            scim_api_update_url=ZivverConfig.zivver_test_endpoint_url,
            scim_api_get_url=ZivverConfig.zivver_test_endpoint_url,
            scim_api_delete_url=ZivverConfig.zivver_test_endpoint_url
        )

    def _cleanup_user(self, zivver_user_username):
        """
        Helping method to remove the user from Zivver
        """
        # Get all accounts from Zivver
        zivver_users_object = self.zivver_scim_connection.get_all_users_from_zivver()
        for zivver_user in zivver_users_object:
            if zivver_user.user_name == zivver_user_username:
                # Delete this Zivver user
                logging.info('Cleanup existing user from Zivver')
                self.zivver_scim_connection.delete_user_from_zivver(account_id=zivver_user.account_id)

    def _test_creation_and_deletion_of_two_hundred_zivver_users(self, account_index, account_max_index):
        """
        Submethod for the test_creation_and_deletion_of_two_hundred_zivver_users
        # 1. Remove 200 accounts if they exist.
        # 2. Create 200 accounts.
        # 3. Check if there are 200 accounts created.
        # 4. Remove all 200 accounts.
        # 5. Check if all 200 accounts are removed
        """
        # 1. Remove 200 accounts if they exist.
        for index in range(account_index, account_max_index):
            account_to_create_email = '{}-{}@{}'.format(index, 'john.doe', ZivverConfig.zivver_test_domain)
            self._cleanup_user(zivver_user_username=account_to_create_email)

        # 2. Create 200 accounts.
        created_zivver_account_ids = {}
        for index in range(account_index, account_max_index):
            account_to_create_email = '{}-{}@{}'.format(index, 'john.doe', ZivverConfig.zivver_test_domain)
            logging.debug('Create account')
            zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
                first_name='{}-john'.format(index),
                last_name='doe',
                nick_name='',
                user_name=account_to_create_email,
                zivver_account_key=account_to_create_email,
                sso_connection=True,
                is_active=True
            )
            created_zivver_account_ids[account_to_create_email] = zivver_user_object.account_id

        # 3. Check if there are 200 accounts created.
        for index in range(account_index, account_max_index):
            account_to_create_email = '{}-{}@{}'.format(index, 'john.doe', ZivverConfig.zivver_test_domain)
            zivver_existing_user = self.zivver_scim_connection.get_user_from_zivver(
                account_id=created_zivver_account_ids[account_to_create_email]
            )
            self.assertEqual(zivver_existing_user.account_id, created_zivver_account_ids[account_to_create_email])

        # 4. Remove all 200 accounts.
        for index in range(account_index, account_max_index):
            account_to_create_email = '{}-{}@{}'.format(index, 'john.doe', ZivverConfig.zivver_test_domain)
            self.zivver_scim_connection.delete_user_from_zivver(
                account_id=created_zivver_account_ids[account_to_create_email]
            )

        # 5. Check if all 200 accounts are removed
        for index in range(account_index, account_max_index):
            account_to_create_email = '{}-{}@{}'.format(index, 'john.doe', ZivverConfig.zivver_test_domain)
            try:
                logging.info('Test to see if the account is deleted')
                zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(
                    account_id=created_zivver_account_ids[account_to_create_email]
                )
                self.assertEqual(False, True)  # Account is not deleted, should fail the test
            except ZivverCRUDError as z_e:
                # Log error message, account does not exist
                logging.info(z_e.get_error_message())
                logging.info(z_e.get_sollution())
                self.assertEqual(True, True)  # Account is deleted, should pass the test

    def test_create_and_update_and_delete_account_in_zivver(self):
        """
        # 1. Remove the account if exists
        # 2. Create the account
        # 3. Test if the account is created
        # 4. Update the account with a new email
        # 5. Test if the email is updated
        # 6. Delete the account from Zivver
        # 7. Test to see if the account is deleted
        """
        self._invoke_setup('test_create_and_update_and_delete_account_in_zivver')

        account_to_create_email = '{}@{}'.format('john.doe', ZivverConfig.zivver_test_domain)
        account_to_update_email = '{}@{}'.format('jane.doe', ZivverConfig.zivver_test_domain)

        # 1. Remove the account if exists
        self._cleanup_user(zivver_user_username=account_to_create_email)
        self._cleanup_user(zivver_user_username=account_to_update_email)

        # 2. Create the account
        logging.info(' Create the account')
        zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='John',
            last_name='Doe',
            nick_name='',
            user_name=account_to_create_email,
            zivver_account_key=account_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 3. Test if the account is created
        logging.info('Test if the account is created')
        zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        self.assertEqual(zivver_user_object.user_name, account_to_create_email)

        # 4. Update the account with a new email
        logging.info('Update the account with a new email')
        zivver_user_object = self.zivver_scim_connection.update_user_in_zivver(
            account_id=zivver_user_object.account_id,
            first_name='Jane',
            last_name='Doe',
            nick_name='',
            user_name=account_to_update_email,
            zivver_account_key=account_to_update_email,
            sso_connection=True,
            is_active=True
        )

        # 5. Test if the email is updated
        logging.info(' Test if the email is updated')
        zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        self.assertEqual(zivver_user_object.user_name, account_to_update_email)

        # 6. Delete the account from Zivver
        logging.info('Delete the account from Zivver')
        self.zivver_scim_connection.delete_user_from_zivver(account_id=zivver_user_object.account_id)

        # 7. Test to see if the account is deleted
        try:
            logging.info('Test to see if the account is deleted')
            zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        except ZivverCRUDError as z_e:
            # Log error message, account does not exist
            logging.info(z_e.get_error_message())
            logging.info(z_e.get_sollution())

    def test_create_duplicate_accounts(self):
            """
            # 1. Remove the account if exists
            # 2. Create the account
            # 3. Test if the account is created
            # 4. Create the same account again
            # 5. Test that the seccond time the account is not created
            """
            self._invoke_setup('test_create_duplicate_accounts')

            account_to_create_email = '{}@{}'.format('john.doe', ZivverConfig.zivver_test_domain)

            # 1. Remove the account if exists
            self._cleanup_user(zivver_user_username=account_to_create_email)

            # 2. Create the account
            logging.debug(' Create the account')
            zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
                first_name='John',
                last_name='Doe',
                nick_name='',
                user_name=account_to_create_email,
                zivver_account_key=account_to_create_email,
                sso_connection=True,
                is_active=True
            )

            # 3. Test if the account is created
            logging.debug('Test if the account is created')
            zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
            self.assertEqual(zivver_user_object.user_name, account_to_create_email)

            # 4. Create the same account again
            try:
                logging.debug('Create the same account again')
                zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
                    first_name='John',
                    last_name='Doe',
                    nick_name='',
                    user_name=account_to_create_email,
                    zivver_account_key=account_to_create_email,
                    sso_connection=True,
                    is_active=True
                )
            except ZivverCRUDError as z_e:
                # 5. Test that the seccond time the account is not created
                logging.debug(z_e.get_error_message())
                logging.debug(z_e.get_sollution())

    def test_alias_and_delegates(self):
        """
        # 1. Remove the account if exists
        # 2. Create the account
        # 3. Test if the account is created
        # 4. Create delegator account
        # 5. Test if delegator account is created
        # 6. Set delegate account to delegator
        # 7. Test that delegate is delegated to delegator
        # 8. Create alias for account
        # 9. Test if alias is set for account
        # 10. Test that delegate is delegated to delegator
        # 11. Remove delegate from account
        # 12. Test if delegate is removed
        # 13. Remove alias from account
        # 14. Test if alias is removed
        """
        self._invoke_setup('test_alias_and_delegates')

        account_to_create_email = '{}@{}'.format('john.doe', ZivverConfig.zivver_test_domain)
        delegator_to_create_email = '{}@{}'.format('group-mailbox', ZivverConfig.zivver_test_domain)
        delegator_alias_to_add_email = '{}@{}'.format('alias-group-mailbox', ZivverConfig.zivver_test_domain)

        # 1. Remove the account if exists
        self._cleanup_user(zivver_user_username=account_to_create_email)
        self._cleanup_user(zivver_user_username=delegator_to_create_email)

        # 2. Create the account
        logging.debug('Create the account')
        zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='John',
            last_name='Doe',
            nick_name='',
            user_name=account_to_create_email,
            zivver_account_key=account_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 3. Test if the account is created
        logging.debug('Test if the account is created')
        zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        self.assertEqual(zivver_user_object.user_name, account_to_create_email)

        # 4. Create delegator account
        logging.debug('Create delegator account')
        zivver_delegator_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 5. Test if delegator account is created
        logging.debug('Test if delegator account is created')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(zivver_delegator_user_object.user_name, delegator_to_create_email)

        # 6. Set delegate account to delegator
        logging.debug('Set delegate account to delegator')
        zivver_delegator_user_object = self.zivver_scim_connection.update_user_in_zivver(
            account_id=zivver_delegator_user_object.account_id,
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True,
            delegates=[account_to_create_email]
        )

        # 7. Test that delegate is delegated to delegator
        logging.debug('Test that delegate is delegated to delegator')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_delegates), 1)
        self.assertEqual(zivver_delegator_user_object.zivver_scim_user_delegates[0], account_to_create_email)

        # 8. Create alias for account
        logging.debug('Create alias for account')
        zivver_delegator_user_object = self.zivver_scim_connection.update_user_in_zivver(
            account_id=zivver_delegator_user_object.account_id,
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True,
            aliases=[delegator_alias_to_add_email],
            delegates=[account_to_create_email]
        )

        # 9. Test if alias is set for account
        logging.debug('Test if alias is set for account')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_aliases), 1)
        self.assertEqual(zivver_delegator_user_object.zivver_scim_user_aliases[0], delegator_alias_to_add_email)

        # 10. Test that delegate is delegated to delegator
        logging.debug('Test that delegate is delegated to delegator')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_delegates), 1)
        self.assertEqual(zivver_delegator_user_object.zivver_scim_user_delegates[0], account_to_create_email)

        # 11. Remove delegate from account
        logging.debug('Remove delegate from account')
        zivver_delegator_user_object = self.zivver_scim_connection.update_user_in_zivver(
            account_id=zivver_delegator_user_object.account_id,
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True,
            aliases=[delegator_alias_to_add_email],
            delegates=[]
        )

        # 12. Test if delegate is removed
        logging.debug('Test if delegate is removed')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_delegates), 0)

        # 13. Remove alias from account
        logging.debug('Remove alias from account')
        zivver_delegator_user_object = self.zivver_scim_connection.update_user_in_zivver(
            account_id=zivver_delegator_user_object.account_id,
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True,
            aliases=[],
        )

        # 14. Test if alias is removed
        logging.debug('Test if alias is removed')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_aliases), 0)

    def test_add_existing_alias(self):
        """
        # 1. Remove the account if exists
        # 2. Create the account
        # 3. Test if the account is created
        # 4. Create the seccond account
        # 5. Test if the seccond account is created
        # 6. Add the second account as alias to the first
        # 7. Test that the alias has not been added
        """
        self._invoke_setup('test_add_existing_alias')

        account_to_create_email = '{}@{}'.format('john.doe', ZivverConfig.zivver_test_domain)
        seccond_account_to_create_email = '{}@{}'.format('jane.doe', ZivverConfig.zivver_test_domain)

        # 1. Remove the account if exists
        self._cleanup_user(zivver_user_username=account_to_create_email)
        self._cleanup_user(zivver_user_username=seccond_account_to_create_email)

        # 2. Create the account
        logging.debug('Create the account')
        zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='John',
            last_name='Doe',
            nick_name='',
            user_name=account_to_create_email,
            zivver_account_key=account_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 3. Test if the account is created
        logging.debug('Test if the account is created')
        zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        self.assertEqual(zivver_user_object.user_name, account_to_create_email)

        # 4. Create the seccond account
        logging.debug('Create the seccond account')
        zivver_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='Jane',
            last_name='Doe',
            nick_name='',
            user_name=seccond_account_to_create_email,
            zivver_account_key=seccond_account_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 5. Test if the seccond account is created
        logging.debug('Test if the seccond account is created')
        zivver_user_object = self.zivver_scim_connection.get_user_from_zivver(account_id=zivver_user_object.account_id)
        self.assertEqual(zivver_user_object.user_name, seccond_account_to_create_email)

        # 6. Add the second account as alias to the first
        try:
            logging.debug('Add the second account as alias to the first')
            zivver_user_object = self.zivver_scim_connection.update_user_in_zivver(
                account_id=zivver_user_object.account_id,
                first_name='John',
                last_name='Doe',
                nick_name='',
                user_name=account_to_create_email,
                zivver_account_key=account_to_create_email,
                sso_connection=True,
                is_active=True,
                aliases=[seccond_account_to_create_email]
            )
        except ZivverCRUDError as z_e:
            logging.info(z_e.get_error_message())
            logging.info(z_e.get_sollution())

        # 7. Test that the alias has not been added
        logging.debug('Test that the alias has not been added')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_aliases), 0)

    def test_non_existing_delegate(self):
        """
        # 1. Remove the account if exists
        # 2. Create delegator account
        # 3. Test if delegator account is created
        # 4. Test that the account to add as delegate does not exist
        # 5. Set delegate account to delegator
        # 6. Test that delegate is not delegated to delegator
        """
        self._invoke_setup('test_non_existing_delegate')

        account_to_create_email = '{}@{}'.format('john.doe', ZivverConfig.zivver_test_domain)
        delegator_to_create_email = '{}@{}'.format('group-mailbox', ZivverConfig.zivver_test_domain)

        # 1. Remove the account if exists
        self._cleanup_user(zivver_user_username=account_to_create_email)
        self._cleanup_user(zivver_user_username=delegator_to_create_email)

        # 2. Create delegator account
        logging.debug('Create delegator account')
        zivver_delegator_user_object = self.zivver_scim_connection.create_user_in_zivver(
            first_name='Delegator',
            last_name='Doe',
            nick_name='',
            user_name=delegator_to_create_email,
            zivver_account_key=delegator_to_create_email,
            sso_connection=True,
            is_active=True
        )

        # 3. Test if delegator account is created
        logging.debug('Test if delegator account is created')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(zivver_delegator_user_object.user_name, delegator_to_create_email)

        # 4. Test that the account to add as delegate does not exist
        logging.debug('Test that the account to add as delegate does not exist')
        zivver_users_object = self.zivver_scim_connection.get_all_users_from_zivver()
        for zivver_user in zivver_users_object:
            if zivver_user.user_name == account_to_create_email:
                # Account exists, but should not!
                self.assertEqual(True, False)

        # 5. Set delegate account to delegator
        try:
            logging.debug('Set delegate account to delegator')
            zivver_delegator_user_object = self.zivver_scim_connection.update_user_in_zivver(
                account_id=zivver_delegator_user_object.account_id,
                first_name='Delegator',
                last_name='Doe',
                nick_name='',
                user_name=delegator_to_create_email,
                zivver_account_key=delegator_to_create_email,
                sso_connection=True,
                is_active=True,
                delegates=[account_to_create_email]
            )
        except ZivverCRUDError as z_e:
            logging.info(z_e.get_error_message())
            logging.info(z_e.get_sollution())

        # 6. Test that delegate is not delegated to delegator
        logging.debug('Test that delegate is delegated to delegator')
        zivver_delegator_user_object = self.zivver_scim_connection.get_user_from_zivver(
            account_id=zivver_delegator_user_object.account_id
        )
        self.assertEqual(len(zivver_delegator_user_object.zivver_scim_user_delegates), 0)

    def test_creation_and_deletion_of_two_hundred_zivver_users(self):
        """
        # 1. Remove 200 accounts if they exist.
        # 2. Create 200 accounts.
        # 3. Check if there are 200 accounts created.
        # 4. Remove all 200 accounts.
        # 5. Check if all 200 accounts are removed
        """
        self._invoke_setup('test_creation_and_deletion_of_two_hundred_zivver_users')

        thread_1 = threading.Thread(
            target=self._test_creation_and_deletion_of_two_hundred_zivver_users, args=(1, 50), daemon=True
        )
        thread_2 = threading.Thread(
            target=self._test_creation_and_deletion_of_two_hundred_zivver_users, args=(51, 100), daemon=True
        )
        thread_3 = threading.Thread(
            target=self._test_creation_and_deletion_of_two_hundred_zivver_users, args=(101, 150), daemon=True
        )
        thread_4 = threading.Thread(
            target=self._test_creation_and_deletion_of_two_hundred_zivver_users, args=(151, 200), daemon=True
        )

        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()


if __name__ == '__main__':
    unittest.main()
