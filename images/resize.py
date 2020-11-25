from PIL import Image


old_im = Image.open('./fullsize/full_Cycling.png')
old_size = old_im.size

new_size = (166, 116)
new_im = Image.new("RGB", new_size, 'white')
new_im.paste(old_im, (round((new_size[0]-old_size[0])/2),
                      round((new_size[1]-old_size[1])/2)))

# new_im.show()
new_im.save('./Cycling2.png')