# azure-storage-blob==2.1.0
from azure.storage.blob import BlockBlobService

class DownloadAzureStorage:
    @classmethod
    def get_blob(self, account_name='', account_key='', path='', blob_path=''):
         # Azure configs
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )

        # create blob base object
        generator = block_blob_service.list_blobs(path)

        # create blob content variable
        blob_content = None

        # loop in all blobs from this path
        for blob in generator:
            # check if blob_name is equals to target blob
            if blob_path == blob.name:
                blob_content = block_blob_service.get_blob_to_bytes(path, blob_path).content.decode('utf8')

        # return content
        return blob_content


    @classmethod
    def get_latest_blob(self, account_name='', account_key='', path='', store_name=''):
        """
        Foi criada essa funcao para coletar o ultimo arquivo da loja e armazenar o conteudo para se integrar 
        com o Napp HUB.
        """
        # Azure configs
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )

        # create blob base object
        generator = block_blob_service.list_blobs(path)
        
        # date objects
        selected_last_modified = None
        selected_file_name = None
        selected_file_content = None
        
        # loop in all blob from generator
        for blob in generator:
            # get file name and last modified date
            file_name = blob.name
            
            # split blob name
            file_name_split = file_name.split('/')

            # create a match name ex: project/store
            match_name = f'{file_name_split[0]}/{file_name_split[1]}'

            if store_name != match_name:
                continue
                
            file_last_modified = blob.properties.last_modified

            # if selected last modified date is not None
            if selected_last_modified:
                # check if selected file  date is greater than current loop file
                if selected_last_modified > file_last_modified:
                    # log
                    log.info(f'This file {selected_file_name} is newest... Skip: {file_name}')
                else:
                    # set dates with this loop file
                    selected_last_modified = file_last_modified
                    selected_file_name = file_name
            else:
                # set dates with this loop file
                selected_last_modified = file_last_modified
                selected_file_name = file_name
        
        # get blob content
        if selected_file_name:
            selected_file_content = block_blob_service.get_blob_to_bytes(path, selected_file_name).content.decode('utf8')
            
            # print
            print(f'Selected file: {selected_file_name}, File date: {selected_last_modified}')
        
            # return blob content
            return selected_file_content
        
        # log with no match files
        print(f'No files detected for this store {store_name}...')
        return None