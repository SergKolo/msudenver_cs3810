import os,sys,json,subprocess
import audioread 
from hashlib import sha256
from gi.repository import Gio,GLib
from PIL import Image,ExifTags

""" This module serves to obtain file-specific information and
    primarily intended for working with files, rather than database
    itself. It can be considered a bridge between database and the
    filesystem """

def get_content_type(fpath):
    """ Determines major/minor type of file and default application
        for given full path of file"""
    try:
        f = Gio.File.new_for_path(fpath)
        info = f.query_info('standard::content-type',0,None)
        ftype = info.get_attribute_as_string('standard::content-type').split('/')
        try:
            app = f.query_default_handler()
            appid = app.get_id()
        except Exception as e2:
            appid = None
        result = tuple(ftype+[appid])
        return result
    except Exception as e:
        print("Exception encountered for file {0}:\n{1}",fpath,e)


def get_metadata(fpath,ftype_major,ftype_minor):
    """ Factory function for returning metadat about a file in 
        json format.This is intended to be called by triggers 
        to insert data into sqlite database. 
    """

    def get_text_meta(fpath):
        out = subprocess.check_output(['wc',fpath]).decode()
        parts = out.split() 
        return json.dumps({ 'newlines': parts[0],
                            'words':parts[1],
                            'bytes':parts[2] })

    def get_audio_meta(fpath):
        try:
            with audioread.audio_open(fpath) as fd:
                 return json.dumps({ 'channel': fd.channels,
                          'samplerate': fd.samplerate,
                          'duration': fd.duration })
        except:
            return None


    def get_exif(fpath):
        try:
            img = Image.open(fpath)
            if not hasattr(img,'_getexif'):
                return json.dumps({'noexif':'noexif'})

            exif_dict={}
            if img._getexif():
                for k,v in img._getexif().items():
                    tag = ExifTags.TAGS[k]
                    #value = v.decode() if v is bytes else str(v)
                    value = str(v)
                    if tag in ['XPTitle', 'XPComment', 'XPAuthor', 'XPKeywords', 'XPSubject']:
                        value = v.decode('utf-16').rstrip('\x00')
                    if tag == 'MakerNote':
                        value = 'SKIPPED'
                    exif_dict[tag] = value
                return json.dumps(exif_dict)

        except Exception as e:
            print(fpath,ftype_minor,e)

    if ftype_major == 'text':
       return get_text_meta(fpath) 
    if ftype_major == 'image' and ftype_minor == 'jpeg':
       return get_exif(fpath)
    if ftype_major == 'audio':
       return get_audio_meta(fpath)
    else:
        return "{ 'NOT IMPLEMENTED': 'NOT IMPLEMENTED' }"

def get_user_dirs(*args):
    """ Returns the standard XDG directories for traversal """
    user_dirs = []
    for index,val in GLib.UserDirectory.__enum_values__.items():
        if index == 8: continue
        directory = GLib.get_user_special_dir(index)
        if directory: user_dirs.append(directory)
    return user_dirs

def walk_home_tree():
    """ Function traverses the directory tree
        and obtains filetype"""
    # TODO: rewrite this !!!!!
    u_dirs = get_user_dirs()
    print(":::DEBUG:",u_dirs)   
    # For now we're only concerned with user's main directories 
    for dirname in u_dirs:
        for root,dir_list,file_list in os.walk(dirname):
            for f in file_list:
                # get relative path for filename
                # then full path. Doesn't concern with links
                r_path = os.path.join(root,f)
                f_path = os.path.abspath(r_path)
                f_stat = os.lstat(f_path)
                content = get_content_type(f_path)
                if content[0] == 'inode':
                    continue
                # TODO: What to do with symlinks ???
                sha256sum = get_sha256sum(f_path,None)
                yield (r_path,f_stat.st_ino,f_stat.st_size,
                       content[0],content[1],sha256sum,content[2])

def get_sha256sum(file_path,type):
    """ reads file and determines SHA 256 hashsum"""
    if type == 'inode/symlink':
        return None
    sha256sum = sha256()
    with open(file_path, 'rb') as fd:
        data_chunk = fd.read(1024)
        while data_chunk:
              sha256sum.update(data_chunk)
              data_chunk = fd.read(1024)
    return str(sha256sum.hexdigest())


if __name__ == '__main__':
    for i in walk_home_tree():
        print(i)
