from io import BytesIO

from django.core.files import File

from example.tests import ViewTestCase

from ...models import PublicFile, PrivateFile


class DriveViewTests(ViewTestCase):
    view_name = 'drive'

    description = 'd'

    name = 'n'

    content = b'c'

    n = 3

    def create(self, description, name, content, DriveFile):
        data = File(BytesIO(content), name)
        file = DriveFile(description=description, data=data)
        file.save()

    def testWithoutFiles(self):
        html = self.html()
        self.assertEqual(0, len(html.select('.full')))
        self.assertEqual(2, len(html.select('.empty')))

    def testWithSinglePublicFile(self):
        self.create(self.description, self.name, self.content, PublicFile)
        html = self.html()
        li = html.select_one('.public li')
        a = li.select_one('a')
        p = li.select('p')[1]
        self.assertEqual(self.name, self.string(a))
        self.assertEqual(self.description, self.string(p))
        empty = html.select_one('.empty')
        self.assertEqual('No private files added.', self.string(empty))

    def testWithSinglePrivateFile(self):
        self.create(self.description, self.name, self.content, PrivateFile)
        html = self.html()
        li = html.select_one('.private li')
        a = li.select_one('a')
        p = li.select('p')[1]
        self.assertEqual(self.name, self.string(a))
        self.assertEqual(self.description, self.string(p))
        empty = html.select_one('.empty')
        self.assertEqual('No public files added.', self.string(empty))

    def testWithSinglePublicFileAndSinglePrivateFile(self):
        self.create(self.description, self.name, self.content, PublicFile)
        self.create(self.description, self.name, self.content, PrivateFile)
        html = self.html()
        self.assertEqual(2, len(html.select('.full')))
        self.assertEqual(0, len(html.select('.empty')))

    def testWithMultiplePublicFiles(self):
        for i in range(self.n):
            self.create(self.description, '{}{}'.format(self.name, i), self.content, PublicFile)
        html = self.html()
        self.assertEqual(self.n, len(html.select('.public li')))

    def testWithMultiplePrivateFiles(self):
        for i in range(self.n):
            self.create(self.description, '{}{}'.format(self.name, i), self.content, PrivateFile)
        html = self.html()
        self.assertEqual(self.n, len(html.select('.private li')))
