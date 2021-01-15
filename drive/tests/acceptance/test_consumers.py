import os

from example.tests import AcceptanceAsyncTestCase, Keys


class ConsumerTests(AcceptanceAsyncTestCase):
    description = 'description'

    def upload(self, files_dir, private):
        names = os.listdir(files_dir)

        selector = '.private' if private else '.public'

        for i, name in enumerate(names):
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

            folder = self.wait(5, self.driver.find_enabled, selector)
            li = self.wait(5, folder.find_exactly, i + 1, 'li')[i]

            a = li.find_one('a')
            p = li.find('p')[1]

            self.assertEqual(name, self.read(a))
            self.assertEqual(description, self.read(p))

        for i in range(len(names), 0, -1):
            folder = self.wait(5, self.driver.find_enabled, selector)
            li = self.wait(5, folder.find_exactly, i, 'li')[0]

            a = self.wait(5, li.find_exactly, 2, 'a')[1]
            a.click()

            input_submit = self.driver.find_one('input[type="submit"]')
            input_submit.click()

    def testUpload(self):
        self.get('drive')
        files_dir = self.files_dir(__file__)
        self.upload(files_dir, False)
        self.upload(files_dir, True)


    content = 'content'

    def contentInLog(self):
        return self.content in self.read(self.driver.find_one('.log'))

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
