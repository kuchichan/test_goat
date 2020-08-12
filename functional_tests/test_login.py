import re
import os
import time
import poplib
from django.core import mail
from selenium.webdriver.common.keys import Keys


from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.zoho.eu')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['INTERIA_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(len(inbox.list()[1]))):
                    _, lines, __ = inbox.retr(i+1)
                    lines = [l.decode('utf-8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
                                              

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # And notices new function "log in" in the navbar
        # So she enter the email
        if self.staging_server:
            test_mail = 'dudarz@zohomail.eu'
        else:
            test_mail = 'edith@example.com'
        
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_mail)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email
        time.sleep(5) # workaround for too fast checks 
        body = self.wait_for_email(test_mail, SUBJECT)

        # It has an unique url in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)

        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        print(url)
        # She clicks it
        self.browser.get(url)
        
        # She is logged in
        self.wait_to_be_logged_in(email=test_mail)

        # She is logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_mail)

                      
