import exiftool
import os 
import xattr


file_path = os.path.join(os.getcwd(), "test.txt")
# add matadata 
print(xattr.setxattr(file_path, "user.gailbot", bytes("gailbot", 'utf-8')))
# compare metadata
print(bytes("gailbot", "utf-8") == xattr.getxattr(file_path, "user.gailbot"))
# type is bytes 
print(type(xattr.getxattr(file_path, "user.gailbot")))
print(xattr.listxattr(file_path))

  