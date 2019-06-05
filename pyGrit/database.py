from blob import Blob
import zlib
import hashlib
import tempfile
import os

class Database():
    """docstring for Database"""
    def __init__(self, path):
        self.path = path

    def store(self, obj):
        _string = obj.to_s
        _string_in_bytes = _string.encode('utf-8')

        content = f"{obj.type} {len(_string_in_bytes)}\0{_string}".encode('utf-8')
        
        # get SHA1 hash after concatenating information, but before compressing.
        # This is done because if you hash after compression, you can't be sure 
        # the compression of the same file will hash to the same hash.
        
        hash_object = hashlib.sha1(content)
        obj.object_id = hash_object.hexdigest()
        self.write_object(obj.object_id, content)
        
        #zlib.compress(sys.stdin.buffer.read()).decode(\"ISO-8859-1\"))
	
    def write_object(self, object_id, content):
        """
        The path to an object is created by obtaining the first two 
        characters from the hashed (SHA1) object ID to use as parent folder 
        and the subfolder is created with the remaining characters.
        
        For example, say we have:
        object_id = 903a71ad300d5aa1ba0c0495ce9341f42e3fcd7c
        
        The location for the object to be created is then:
        '.../.git/objects/90/3a71ad300d5aa1ba0c0495ce9341f42e3fcd7c'
        """
        
        object_path = os.path.join(self.path, object_id[:2], object_id[2:]) # path to write
        dir_name = os.path.dirname(object_path) # parent folder
        
        if not os.path.exists(dir_name):
            # permanently create the folder named object_id[:2]
            # and then write the contents of the object.
            try:
                os.makedirs(dir_name)	
            except OSError as err:
                logging.error(f'Error: Creating {dir_name}: {err}')
                exit(1)

        # create temporary file in the directory you'll write 
        # so as to atomically move it to its real name after writing finishes up.
        tmp_file = tempfile.NamedTemporaryFile(dir=dir_name, delete=False) 
        try: 
            compressed_content = zlib.compress(content, 1) # 1 means best speed, least compression.
            tmp_file.write(compressed_content)
            tmp_file.close()
        except:
            logging.error(f'Could not write to {tmp_file}')

        os.rename(tmp_file.name, object_path)
