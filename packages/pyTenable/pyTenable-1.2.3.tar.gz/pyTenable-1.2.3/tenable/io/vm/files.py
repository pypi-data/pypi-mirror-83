'''
Files
=====

Methods described in this section relate to the the files API under the vm
section.  These methods can be accessed at
``TenableIO.vm.files``.

.. rst-class:: hide-signature
.. autoclass:: FilesAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint


class FilesAPI(APIEndpoint):
    _path = 'file'

    def upload(self, fobj, encrypted=False):
        '''
        Uploads a file into Tenable.io.

        :devportal:`file: upload <file-upload>`

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable.io.
            encrypted (bool, optional):
                If the file is encrypted, set the flag to True.

        Returns:
            :obj:`str`:
                The fileuploaded attribute

        Examples:
            >>> with open('file.txt') as fobj:
            ...     file_id = tio.files.upload(fobj)
        '''
        kwargs = dict(files={'Filedata': fobj})
        if encrypted:
            kwargs['data'] = {'no_enc': int(encrypted)}
        return self._api.post('upload', **kwargs).fileuploaded