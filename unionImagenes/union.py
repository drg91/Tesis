import numpy as np
from PIL import Image

def unir(img1,img2,img3,img4,imgSalida):
    images_list = [img1+'.jpg',img2+'.jpg',img3+'.jpg',img4+'.jpg']
    imgs = [ Image.open(i) for i in images_list ]
    min_img_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    img_merge = np.hstack( (np.asarray( i.resize(min_img_shape,Image.ANTIALIAS) ) for i in imgs ) )
    img_merge = Image.fromarray( img_merge)
    img_merge.save( imgSalida+'.jpg' )
    print "Imagenes Unidas: "+img1 + " "+img2+ " "+img3+ " "+img4

unir('1', '2', '3' , '4', 'unida')
