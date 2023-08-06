def gdplot():

    import gspread #pip install gspread
    import pandas as pd
    import matplotlib.pyplot as plt

    """
    For taking input from google drive we have to first create a login using a google account on https://console.developers.google.com
    and add api for Google Drive and Google Sheets. After Adding these API's we have to create a service account to and get the json file for 
    user credentials. The file needs to be downloaded and path to be provided below.
    """

    cred_file = input("Enter Credential file path :")

    # gc =gspread.service_account(filename= 'creds.json')
    """
    Using the Credentials extracting the gdrive account of the user
    
    """

    gc =gspread.service_account(filename= cred_file)

    """
    We need the key of the gsheet we are trying to access. To get the key open the file in the browser. From the link
    which will look something like this : "https://docs.google.com/spreadsheets/d/1XuAgQnL3W80EuHv7kkHU2q_Y-LpdgsCuiYxThba6cyo/edit#gid=1127594002"
    . This is the key of the file we need. We will extract the first sheet from the gsheet.
    """
    key = input("Enter the gsheet file key : ")
    # sh = gc.open_by_key('1XuAgQnL3W80EuHv7kkHU2q_Y-LpdgsCuiYxThba6cyo')
    sh = gc.open_by_key(key)
    worksheet = sh.sheet1

    """
    Saving the Gsheet as a Pandas Dataframe and printing the first five results of the Dataframe.
    """
    dataframe = pd.DataFrame(worksheet.get_all_records())
    print("First 5 records of the Data : ")
    print(dataframe.head() )

    """
    We have developed the code only for two types of graphs i.e. Line plot and Scatter plot.
    """

    type_of_graph = input("Type of Graph (line/scatter) :")

    """
    If the user selects line plot plt.plot will plot a single line graph
    .If the user selects scatter plot plt.scatter will plot a scatter plot graph.
    
    """

    if type_of_graph == "line":
        x = input("Input x axis : ")
        y = input("Input y axis : ")
        plt.xlabel(str(x))
        plt.ylabel(str(y))
        plt.title(str(x)+" v/s "+ str(y))
        plt.plot(dataframe[x], dataframe[y])
        plt.show()

    elif type_of_graph == "scatter":
        x = input("Input x axis : ")
        y = input("Input y axis : ")
        plt.xlabel(str(x))
        plt.ylabel(str(y))
        plt.title(str(x)+" v/s "+ str(y))
        plt.scatter(dataframe[x], dataframe[y] )
        plt.show()

    else :
        print("Wrong Type of Graph")
