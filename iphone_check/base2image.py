from sys import argv, exit
import os
import base64
import imghdr

b64_data = 

image_data = base64.b64decode(b64_data)
image_type = imghdr.what('', image_data)

destination_file_name = "file_base_name" + '_converted.' + image_type

destination = open(destination_file_name, 'wb')
destination.write(image_data)
destination.close()