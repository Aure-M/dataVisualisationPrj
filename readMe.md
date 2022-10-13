## DataVisualisation project

#### Data exploration and cleaning
1. The data exploring and cleaning step was done in `./dataVisu.ipynb`. I've worked on the `2020` and `2019` dataset.
2. After cleaning the data the results were saved in `df2020.csv` `df2019.csv`

<br /><br />

#### Streamlit app
1. The streamlit app have three main feature.<br />
    a. 2019 analysis : This feature allows you to have an overview of the 2019 data and to focus on a particular municipality<br /><br />
    b. 2020 analysis : This feature allows you to have an overview of the 2020 data and to focus on a particular municipality<br /><br />
    c. filter feature : This feature helps you to have an overview of the 2020 data with a filter. You can also download the filtered data after for your own purpose.<br /><br />
2. Files architecture:<br />
    a. `./prj_utils.py` contains all the function that were used to process/visualize the data <br /><br />
    b. `./project.py` is the main file of the app<br /><br />
3. If you are struggling to run the app, you can access it on the stremlit servers with this link --> https://aure-m-datavisualisationprj-project-sf88ef.streamlitapp.com