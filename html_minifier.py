from minify_html import minify_html as mh
import os
directory = os.path.join(os.path.dirname(__file__),'KeyClub_Flask_Setup/website/templates')
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)

    with open(filename,"r+") as file:
        text = file.read()
        processed_html = mh.minify(text)
        print(processed_html)
        #file.write(processed_html)