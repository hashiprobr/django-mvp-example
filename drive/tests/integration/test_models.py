from io import BytesIO

from django.core.files import File
from django.db import IntegrityError

from example.tests import IntegrationTestCase

from ...models import PublicFile, PrivateFile


class FileTests:
    description = 'd'

    name = 'n'
    other_name = 'on'

    content = b'c'
    other_content = b'oc'

    def open(self, name, content):
        return File(BytesIO(content), name)

    def create(self, description, name, content):
        data = self.open(name, content)
        return self.DriveFile.objects.create(description=description, data=data)

    def retrieve(self, name, content):
        data = self.open(name, content)
        return self.DriveFile.objects.filter(data=data).exists()

    def delete(self, name, content):
        data = self.open(name, content)
        self.DriveFile.objects.filter(data=data).delete()

    def assertDoesNotCreate(self, description, name, content):
        with self.assertRaises(IntegrityError):
            self.create(description, name, content)

    def assertRetrieves(self, name, content):
        self.assertTrue(self.retrieve(name, content))

    def assertDoesNotRetrieve(self, name, content):
        self.assertFalse(self.retrieve(name, content))

    def assertDataExists(self, name):
        self.assertTrue(self.DriveFile.data.field.storage.exists(name))

    def assertDataDoesNotExist(self, name):
        self.assertFalse(self.DriveFile.data.field.storage.exists(name))

    def testDoesNotCreateWithNoneDescription(self):
        self.assertDoesNotCreate(None, self.name, self.content)

    def testRetrievesByNameAfterCreate(self):
        self.create(self.description, self.name, self.content)
        self.assertRetrieves(self.name, self.other_content)

    def testDoesNotRetrieveByContentAfterCreate(self):
        self.create(self.description, self.name, self.content)
        self.assertDoesNotRetrieve(self.other_name, self.content)

    def testDoesNotRetrieveAfterCreateAndDeleteByName(self):
        self.create(self.description, self.name, self.content)
        self.delete(self.name, self.other_content)
        self.assertDoesNotRetrieve(self.name, self.content)

    def testDataExistsAfterCreate(self):
        self.create(self.description, self.name, self.content)
        self.assertDataExists(self.name)

    def testDataDoesNotExistAfterCreateAndDeleteByName(self):
        file = self.create(self.description, self.name, self.content)
        self.delete(self.name, self.other_content)
        self.assertDataDoesNotExist(self.name)


class PublicFileTests(FileTests, IntegrationTestCase):
    DriveFile = PublicFile


class PrivateFileTests(FileTests, IntegrationTestCase):
    DriveFile = PrivateFile
