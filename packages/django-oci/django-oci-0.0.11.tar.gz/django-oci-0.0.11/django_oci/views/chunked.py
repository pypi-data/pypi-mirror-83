"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.views.generic.base import TemplateView
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django_oci.models import MyChunkedUpload


class ChunkedUploadDemo(TemplateView):
    template_name = "django_oci/chunked_upload.html"


class MyChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = "the_file"

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        print("django_oci:check_permissions")
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        print("django_oci:check_permissions")
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        print("django_oci:on_completion")
        pass

    def get_response_data(self, chunked_upload, request):
        print("django_oci:get_response_data")
        return {
            "message": (
                "You successfully uploaded '%s' (%s bytes)!"
                % (chunked_upload.filename, chunked_upload.offset)
            )
        }
