from io import BytesIO

from django.core.files import File

from example.tests import IntegrationTestCase

from ...models import DriveFile, PublicFile, PrivateFile
from ...forms import FileForm


class FileFormTests(IntegrationTestCase):
    description = 'd'
    blank_description = ''
    upper_description = (DriveFile.description.field.max_length + 1) * 'd'
    other_description = 'od'

    name = 'n'
    other_name = 'on'

    content = b'c'
    blank_content = b''
    other_content = b'oc'

    def open(self, name, content, existing):
        if existing is not None:
            existing_description, existing_name, existing_content, DriveFile = existing
            existing_data = File(BytesIO(existing_content), existing_name)
            file = DriveFile(description=existing_description, data=existing_data)
            file.save()
        return File(BytesIO(content), name)

    def isValid(self, description, uploaded, private):
        data = {}
        files = {}
        if description is not None:
            data['description'] = description
        if uploaded is not None:
            name, content, existing = uploaded
            files['data'] = self.open(name, content, existing)
        if private is not None:
            data['private'] = private
        form = FileForm(data, files)
        return form.is_valid()

    def assertValid(self, description, uploaded, private):
        self.assertTrue(self.isValid(description, uploaded, private))

    def assertNotValid(self, description, uploaded, private):
        self.assertFalse(self.isValid(description, uploaded, private))

    def assertRaisesKeyError(self, description, uploaded, private):
        with self.assertRaises(KeyError):
            self.isValid(description, uploaded, private)

    def testValidWithFalsePrivate(self):
        self.assertValid(self.description, (self.name, self.content, None), False)

    def testValidWithTruePrivate(self):
        self.assertValid(self.description, (self.name, self.content, None), True)

    def testValidWithoutPrivate(self):
        self.assertValid(self.description, (self.name, self.content, None), None)

    def testRaisesKeyErrorWithoutDescriptionAndFalsePrivate(self):
        self.assertRaisesKeyError(None, (self.name, self.content, None), False)

    def testRaisesKeyErrorWithoutDescriptionAndTruePrivate(self):
        self.assertRaisesKeyError(None, (self.name, self.content, None), True)

    def testRaisesKeyErrorWithBlankDescriptionAndFalsePrivate(self):
        self.assertRaisesKeyError(self.blank_description, (self.name, self.content, None), False)

    def testRaisesKeyErrorWithBlankDescriptionAndTruePrivate(self):
        self.assertRaisesKeyError(self.blank_description, (self.name, self.content, None), True)

    def testNotValidWithUpperDescriptionAndFalsePrivate(self):
        self.assertNotValid(self.upper_description, (self.name, self.content, None), False)

    def testNotValidWithUpperDescriptionAndTruePrivate(self):
        self.assertNotValid(self.upper_description, (self.name, self.content, None), True)

    def testRaisesKeyErrorWithoutUploadedAndFalsePrivate(self):
        self.assertRaisesKeyError(self.description, None, False)

    def testRaisesKeyErrorWithoutUploadedAndTruePrivate(self):
        self.assertRaisesKeyError(self.description, None, True)

    def testValidWithBlankContentAndFalsePrivate(self):
        self.assertValid(self.description, (self.name, self.blank_content, None), False)

    def testValidWithBlankContentAndTruePrivate(self):
        self.assertValid(self.description, (self.name, self.blank_content, None), True)

    def testNotValidIfPublicFileWithSameNameExistsAndFalsePrivate(self):
        self.assertNotValid(self.description, (self.name, self.content, (self.other_description, self.name, self.other_content, PublicFile)), False)

    def testNotValidIfPrivateFileWithSameNameExistsAndTruePrivate(self):
        self.assertNotValid(self.description, (self.name, self.content, (self.other_description, self.name, self.other_content, PrivateFile)), True)

    def testValidIfPublicFileExistsAndFalsePrivateButDifferentName(self):
        self.assertValid(self.description, (self.name, self.content, (self.description, self.other_name, self.content, PublicFile)), False)

    def testValidIfPrivateFileExistsAndTruePrivateButDifferentName(self):
        self.assertValid(self.description, (self.name, self.content, (self.description, self.other_name, self.content, PrivateFile)), True)

    def testValidIfPrivateFileWithSameNameExistsButFalsePrivate(self):
        self.assertValid(self.description, (self.name, self.content, (self.description, self.name, self.content, PrivateFile)), False)

    def testValidIfPublicFileWithSameNameExistsButTruePrivate(self):
        self.assertValid(self.description, (self.name, self.content, (self.description, self.name, self.content, PublicFile)), True)
