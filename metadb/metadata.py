import os,sys
from hashlib import sha256
from gi.repository import Gio,GLib
from PIL import Image
from audioread import audio_open


def get_metadata(fpath,ftype):
    """ Factory function for returning metadat about a file in json format.
        This is intended to be called by triggers to insert data into database.
        We should have gotten filetype when inserting into file table,hence two args
    """
    pass

    # https://lazka.github.io/pgi-docs/Gio-2.0/enums.html#Gio.FileType.MOUNTABLE
    # f = Gio.File.new_for_path(f_path)
    # info = f.query_info('standard::content-type',0,None)
    # return info.get_attribute_as_string('standard::content-type')
    # return f.query_file_type(0,None)
    # return Gio.content_type_guess(f,None)

#	def get_exif():
#	    """ TODO """
#	    # python3 -c 'from PIL import Image,ExifTags;import sys;
#	    # print( { ExifTags.TAGS[k]:v  for k,v in Image.open(sys.argv[1])._getexif().items()})'
#	    pass
#
#
#	def get_image_metadata(files):
#	    """generator for tuple image of resolution"""
#	    for i in files:
#		with Image.open(i) as img:
#		     yield img.size
#
#	def get_audio_metadata(files):
#	    """generator for audio channel,sample rate, and duration in sec"""
#	    for i in files:
#		try:
#		    with audio_open(i) as fd:
#			 yield (fd.channels,fd.samplerate,fd.duration)
#		except audioread.NoBackendError as aderr:
#		       print(aderr.__cause__,aderr.__context__,aderr.__dict__)


def get_user_dirs(*args):
    user_dirs = []
    for index,val in GLib.UserDirectory.__enum_values__.items():
        if index == 8: continue
        dir = GLib.get_user_special_dir(index)
        if dir: user_dirs.append(dir)
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
                metadata = get_file_metadata(f_path)
                # TODO: What to do with symlinks ???
                sha256sum = get_sha256sum(f_path,metadata)
                yield (r_path,sha256sum,metadata)

def get_sha256sum(file_path,type):
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
    walk_tree()
