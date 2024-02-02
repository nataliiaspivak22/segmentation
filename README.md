**Welcome to the web app for Customers Segmentation Project.**


# Run a Notebook, web app:

0. Make sure [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) is installed on your PC.

1. Pull current repo:
```buildoutcfg
git clone git@github.com:h-dychko/segmentation.git
```

2. Create a folder `/data` inside the project and put the downloaded data from [Customer Personality Analysis kaggle project](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis) into it.

3. Create a virtual environment and install requirements
```
# Windows, Ubuntu
conda env create -f environment.yml
```

4. a. To run notebooks:   
```
conda activate segmentation

jupyter notebook   
```   

 b. To run application:
```
conda activate segmentation 

streamlit run Start.py
```

## About Repo:
* `/notebooks` contains EDA of customers' data 
* `/data` - .csv file with customers' info to work with
* `/pages` - pages of the web app
