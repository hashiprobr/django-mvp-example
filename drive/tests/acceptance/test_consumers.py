import os

from example.tests import AcceptanceTestCase, Keys


class ConsumerTests(AcceptanceTestCase):
    description = 'description'

    def upload(self, files_dir, private):
        for i, name in enumerate(os.listdir(files_dir)):
            path = os.path.join(files_dir, name)
            description = '{}{}'.format(self.description, i)

            input_data = self.driver.find_one('#id_data')
            input_data.send_keys(path)

            input_description = self.driver.find_one('#id_description')
            input_description.send_keys(description)

            if private:
                input_private = self.driver.find_one('input[type="checkbox"]')
                input_private.click()

            input_submit = self.driver.find_one('input[type="submit"]')
            input_submit.click()

            folder = self.wait(5, self.driver.find_enabled, '.private' if private else '.public')
            self.wait(5, folder.find_one, 'li')
            lis = self.wait(5, folder.find_exactly, i + 1, 'li')
            li = lis[i]

            a = li.find_one('a')
            p = li.find('p')[1]

            self.assertEqual(name, self.text(a))
            self.assertEqual(description, self.text(p))

    def testUpload(self):
        self.get('drive')
        files_dir = self.files_dir(__file__)
        self.upload(files_dir, False)
        self.upload(files_dir, True)


    content = 'content'

    def contentInLog(self):
        return self.content in self.driver.find_one('.log').text

    def testChat(self):
        self.get('drive')
        self.open()
        self.switch(1)
        self.get('drive')
        self.switch(0)
        (self.chains()
            .click(self.driver.find_one('.input'))
            .send_keys(self.content)
            .send_keys(Keys.RETURN)
        ).perform()
        self.wait(2, self.contentInLog)
        self.switch(1)
        self.wait(2, self.contentInLog)
        self.close()
        self.switch(0)
