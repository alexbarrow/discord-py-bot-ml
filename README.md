# discord-py-bot-ml
This code is to implement the machine learning and some statistical functions to discord bot. It contains all stages 
from user input to output the prediction of the model and provides statistical info about dataset by using discord bot commands. The bot is based on `discord.py` library.
 
## Dataset
Original data are stored in `data/data_all.csv` and have specific form. All categorical variables are encoded by certain tags (user can see all tags by `!tags` discord bot command). This was done to easy new data input. New entry to dataset is done with `#stat` discord bot command. After command user has to input required parameters which depend on the dataset. 

## Content
* `bot_main.py`: contains all functions related to bot.
* `data_dict.py`: all dictionary type variables and urls.
* `data_handler.py`: various functions and handlers for inputs and raw data.
* `ml_data.py`: all methods related to preparation of dataset for ML algorithms.
* `ml_nodule.py`: ML models, accuracy functions, etc.
* `data/data_all.csv`: original dataset.
* `ml_data/data_train.csv`: prepared dataset.
