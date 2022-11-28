"""
mountain_fastai.py
by Alder French

Description:
This is supposed to be a super basic image classification model builder that creates a .pkl machine learning
model given a folder with labeled images, built using FastAI.

Sources:
https://docs.fast.ai/tutorial.vision.html
"""

from fastai.vision.all import *

if __name__ == "__main__":
   print("Running mountain_fastai.py...")
   path = "images\\test_images_01\\"
   print("path: " + str(path))
   files = get_image_files(path)
   print(len(files))
   pat = r'^(.*)_\d+.jpg' #Pattern to get label by getting everything before the first space then digit sequence
   # NOTE: path in line below should maybe be changed to reference current directory
   dls = ImageDataLoaders.from_name_re(path, files, pat, item_tfms=Resize(460), batch_tfms=aug_transforms(size=224))
   learn = vision_learner(dls, resnet34, metrics=error_rate)
   learn.lr_find()
   learn.fine_tune(2, 3e-3)
   learn.path = "models/"
   learn.export()

