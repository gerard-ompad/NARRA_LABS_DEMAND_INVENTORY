# Instructions

## Step 1: Very Important Step:

1. This prototpye uses a packaged model and requires libomp to work

2. For Mac users, open your terminal and type:

    brew install libomp 

3. For windows users, things is more complicated, it is suggested to perform Step 2 first, if the dashboard does not work then your system does not have a libgomp-1.dll, to install this go to:

    https://www.dll-files.com/libgomp-1.dll.html

## Step 2: Installing requirements for Mac/Linux/Windows

1. Open your terminal
2. Navigate to the folder ds-interview, if the folder is in the Downloads then in your terminal type:

   cd ./Downloads/ds-interview

3.1 The ds-interview folder contains a yaml file that contains the important libraries used in this analysis. If you are a pip user in your terminal type:

    pip install -r requirements.yaml
    
3.2 If you are a pip3 user, in your terminal type:

    pip3 install -r requirements.yaml --break-system-packages
    
4. To open the dashboard nagivate to the ORDERS_PROD folder by typing in your terminal:

    cd ./ds-interview/ORDERS_PROD
    
5.1 For python version users that are less than 3.0, type the following in your terminal:

   python app.py
   
5.2 For python3 version users, type the following in your terminal:

   python3 app.py
   
6. To know that the run is successful you must be able to see a message in the terminal with the following statement:

    Dash is running on http://127.0.0.1:9000/
    
7. Copy and paste the link http://127.0.0.1:9000/ to any browser.


## Step 3: Dashboard Data Dictionary

1. Order ID = alphanumeric, this is the bill of lading of the order and serves as the primary key reference between the customer, driver, and the platform.

2. Date = The date of order.

3. Time = The time or order.

4. Distance = Distance between the restaurant of origina to the address of distination.

5. Order Quantity = Number of products ordered.

6. Popularity = Ranking of the restuarant, the higher the number then the more popular the restuarant is.

7. Traffic = Traffic Situation.

8. Weather = Weather type during the order {0:"Clear",1:"Cloudy",2:"Fog",3:"Rainy"}.

9. Estimated Delivery Time (minutes) = Predicted total delivery times

10. Submit Button = Clickable button to input the data into the table.

11. Download CSV = Clickable button to download the tabl as a .csv file.


## Step 4: Analysis

1. All analysis along with the explanation can be seen in the DS_INTERVIEW.ipynb

2. You must have a jupyter notebook to open the file.

3. The file contains the reasoning behind:

    **Data Preparation**

    **Exploratory Data Analysis (EDA)**

    **Feature Engineering**

    **Model Building**

    **Results Interpretation and Model Analysis**

    **Recommendations**
    
4. If no interactive plots are seen on the top side of the notebook click "cell", then click "Run All", this will refresh the notebook.

## Step 5: Running and testing  the prediction code using CURL.

1. Open a new terminal and nagivate to the ds-interview folder.

2. **DO NOT NAVIGATE INTO THE ORDERS_PROD**

3. Inside the ds-interview folder you will find another python script entitled app.py, this is different from the app.py inside the ORDERS_PROD folder.

4.1 If your are using python version less than 3.0, in your terminal type:

    python app.py
    
4.2 If you are using python 3.0, in your terminal type:

    python3 app.py
    
5. Open another terminal, to test the prediction code, copy paste the entire code below into your terminal:

    curl -X POST -H "Content-Type: application/json" -d '{"distance_km":5,"order_size":3,"restaurant_popularity":4}' http://127.0.0.1:5000/predict
    
6. In the same terminal where you trigger a curl test you should be able to see the predicted value:

    {
      "predicted_time_to_delivery": 20.104829788208008
    }
    
7. You can further test the code by changing the numbers inside the'{""distance_km":5,"order_size":3,"restaurant_popularity":4}'.


