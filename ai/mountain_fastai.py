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

def main():
   print("Running mountain_fastai.py...")
   path = Path("images/test_cleaner_small/")
   print("path: " + str(path))
   [print(str(f)) for f in path.iterdir() if f.is_file()]
   #files = get_image_files(path)
   files = get_image_files(path)
   print(len(files))
   # Pattern to get label by getting everything before the first space then digit sequence
   pat = r'^(.*)\s\d+.jpg'
   # NOTE: path in line below should maybe be changed to reference current directory
   dls = ImageDataLoaders.from_name_re(
       "./", files, pat, item_tfms=Resize(460), batch_tfms=aug_transforms(size=224))
   learn = vision_learner(dls, resnet34, metrics=error_rate)
   #learn.show_results()
   learn.lr_find()
   learn.fine_tune(2, 3e-3)
   learn.path = Path("models/")
   print("Trained model sucessfully, trying to export...")
   learn.export()

if __name__ == "__main__":
   main()

