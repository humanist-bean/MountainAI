# MountainAI

## Have you ever seen an iconic photo of a mountain, and wondered what mountain it is? Well wonder no more, because MountainAI is here! Inspired by a mysterious but beautiful picture of a mountain I got from a thrift store, MountainAI will try to identify the mountain in any photo you feed it!

### Most of the hard work I've done in this project resides in the "mountain_img_scraper" folder's "mountain_soup.py". This python script uses Selenium with Chrome to scrape bing images given a txt file with 1 search phrase per line. So far it works alright and I've used it to collect up to 75,000 photos in 1 go that took roughly 7 hours. However it still crashes on occasion, so in the future I want to modify it to download images while it searches for them using Python's multithreading, that way if it crashes mid scrape I can start it up where it left off instead of restarting at the beginning of the list. I may also give it the ability to open multiple chrome windows and perform multiple searches at once, as this may not be too tricky if I am going to work with multithreading and thread safe shared data anyways. 

### I used FastAI to train the models that MountainAI uses. FastAI does the heavy lifting training the models and tuning them, so my code here is pretty minimal. In the future, I would love to learn more about the ins and outs of FastAI, and eventually about the Pytorch framework it uses. I will keep updating my models in this repository as I do that and also as I collect more photos for the MountainAI models. Hopefully this results in increasingly accurate MountainAI models and thus better mountain recognition.

### Last but not least my models can be used with the streamlit server whose code resides in the deploy folder. You can run it by downloading deploy/streamlit_server.py and deploy/models, installing the necessary streamlit packages, and then running:
`streamlit run streamlit_server.py`

Note:
This repository is intended for use in a virtual environment with python's "virtualenv" on macOS and unix based systems
AND
is intended for use with an Anaconda "Conda" environment on Windows

