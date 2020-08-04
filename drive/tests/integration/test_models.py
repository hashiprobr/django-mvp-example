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
        file = self.DriveFile(description=description, data=data)
        file.save()

    def retrieve(self, name, content):
        data = self.open(name, content)
        return self.DriveFile.objects.filter(data=data).exists()

    def delete(self, name, content):
        data = self.open(name, content)
        self.DriveFile.objects.filter(data=data).delete()

    def assertRaisesIntegrityErrorIfCreate(self, description, name, content):
        with self.assertRaises(IntegrityError):
            self.create(description, name, content)

    def assertRetrieves(self, name, content):
        self.assertTrue(self.retrieve(name, content))

    def assertDoesNotRetrieve(self, name, content):
        self.assertFalse(self.retrieve(name, content))

    def testRaisesIntegrityErrorIfCreateWithNoneDescription(self):
        self.assertRaisesIntegrityErrorIfCreate(None, self.name, self.content)

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


class PublicFileTests(FileTests, IntegrationTestCase):
    DriveFile = PublicFile


class PrivateFileTests(FileTests, IntegrationTestCase):
    DriveFile = PrivateFile
