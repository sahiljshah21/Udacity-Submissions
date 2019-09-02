import time
import statistics as st 
import pandas as pd 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    """This is a function to get an input for the city filter and check if the input is one of the three cities in the data set.
    Returns: One of the three cities in our data set"""
    
    city = input("\nPick a city to get started: Chicago, New York City, Washington? Please type the city names as shown.\n").lower()
    if city == 'chicago' or city == 'new york city' or city == 'washington':
        return city
    else:
        print("\nOops! Looks like you entered a different city.")
        get_city()

def get_month():
    """This is a function to get an input for the month filter.
    Returns: One of the 12 months or all."""
    
    month = input("\nPlease enter the month for which you need to filter the data. Enter 'all' if you wish to see the data for all 6 months.\n").lower()
    if month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month != 'july' and month != 'all':
        print("\nUmm... We only have data for the first six months of the year. Sorry!")
        get_month()
    return month

def get_day():
    """This is a function to get an input for the day filter.
    Returns: One of the seven days of the week or all."""

    day = input("\nDo you want to further filter the data by the day of the week? If yes, please enter the day. If no, please enter 'all'.\n").lower()
    if day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday' and day != 'all':
        print("You know, there's only so many ways in which you can type out the day of the week... :P")
        get_day()
    return day

def time_stats(df):
    """This is a function that determines the most common month, day and hour, based on the datetime objects in the Start Time column.
    Args: The dataframe object"""

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    #month = int(df.loc[:,'Month'].mode())
    #The above piece of code is printing a zero followed by the mode, and hence I have included the statistics library. 
    month = st.mode(df.loc[:,'Month'])
    print("\nThe most common month is: {}".format(months[month-1].capitalize()))
    day = st.mode(df.loc[:,'Day of the Week'])
    print("\nThe most common day of the week is: {}".format(day))
    hour = st.mode(df.loc[:,'Hour'])
    print("\nThe busiest hour in the day is: {}".format(hour))

def station_stats(df):
    """This is a function that determines the most common start and end stations, and the most popular journey. 
    Args: The dataframe object"""

    #start_station = str(df.loc[:,'Start Station'].mode())
    #Same issue as the previous function. Calling mode on st.
    start_station = st.mode((df.loc[:,'Start Station']))
    print("\nThe most popular start station is: {}".format(start_station))
    end_station = st.mode(df.loc[:,'End Station'])
    print("\nThe most popular end station is: {}".format(end_station))
    popular_journey = st.mode(df.loc[:,'Journey'])
    print("\nThe most popular journey is: {}".format(popular_journey))
    
def trip_duration_stats(df):
    """This is a function that determines the sum and mean of the time taken for all trips for the given filters.
    For easy readability
        1. Separators (,) have been included for the sum - which is in hours.  
        2. Separators (,) have been inclued for the mean, printed as an int in minutes
    Args: The dataframe object"""

    total_time = df.loc[:,'Trip Duration'].sum()
    print("\nThe total duration of all trips taken for the filters selected is: {:,} hours".format(int(total_time/3600)))
    mean_time = int(df.loc[:, 'Trip Duration'].mean()/60)
    print("\nThe average duration per trip for the filters selected is: {:,} minutes".format(mean_time))

def user_stats(df):
    """This is a function that determines the count of users for the filters chosen - by gender and by type. 
    Args: The dataframe object"""

    try:
        user_count = df.groupby(['User Type'])['Start Time'].count()
        print("\n", user_count)
    except KeyError:
        print("\nUmm... Looks like we don't have the user type data for your selection.")
    
    try:
        gender_count = df.groupby(['Gender'])['Start Time'].count()
        print("\n", gender_count)
    except KeyError:
        print("\nLooks like we don't have the gender data for your selection.")

    try:    
        oldest = int(df.loc[:,'Birth Year'].min())
        print("\nThe oldest person in our data was born in: {}".format(oldest))
        youngest = int(df.loc[:,'Birth Year'].max())
        print("\nThe youngest person in our data was born in: {}".format(youngest))
        common_by = int(df.loc[:,'Birth Year'].mode())
        print("\nThe most common birth year is in our data is: {}".format(common_by))
    except KeyError:
        print("\nLooks like we don't have the birth year data for your selection.")

def frame_print(df):
    """This is a function that prints 5 lines of code based on the user's input. 
    Args: The dataframe object"""
    row = 0
    while True:
        n = input("\nWould you like to see the raw data for your filters?\n").lower()
        if n == 'yes':
            print(df.iloc[row:row+5])
            row += 5
        else:
            break


def main():
    while True:
        city = get_city()
        month = get_month()
        day = get_day()
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Month'] = df['Start Time'].dt.month
        df['Day of the Week'] = df['Start Time'].dt.weekday_name
        df['Hour'] = df['Start Time'].dt.hour
        df['Journey'] = df['Start Station'] + " - " + df['End Station']
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['Month'] == month]
        if day != 'all':
            df = df[df['Day of the Week'] == day.title()]
     
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        frame_print(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()


