import imageio
import os

def gif_from_images(path,name):
    filenames = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            print(path+file)
            filenames.append(path+file)
            
    
    with imageio.get_writer(path+name+'.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    
    