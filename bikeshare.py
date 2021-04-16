import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    getCityPrompt = True;
    city = "";
    cities = ['chicago', 'new york city', 'washington']
    while getCityPrompt:
        city = input("Enter Requested City Intials (C, NY, W)\n").lower();
        if city in ['c', 'ny', 'w']:
            getCityPrompt = False;
            i = ['c', 'ny', 'w'].index(city);
            city = cities[i];
        else:
            print("Please Enter one of the given initials");

    # get user input for month (all, january, february, ... , june)
    getMonthPrompt = True;
    month = -1;
    months = [str(i) for i in range(7)]
    while getMonthPrompt:
        month = input("Enter a number from 0 to 6, where 0 represents all months, 1-Jan, 2-Feb,.. 6-June\n");
        if month in months:
            getMonthPrompt = False;
            i = months.index(month);
            month = i;
        else:
            print("Please Enter one of the given numbers");

    getDayPrompt = True;
    day = -1;
    days = [str(i) for i in range(8)]
    while getDayPrompt:
        day = input("Enter a number from 0 to 7, where 0 represents all days, 1-Mon, 2-Tues,... , 7-Sun\n");
        if day in days:
            getDayPrompt = False;
            i = days.index(day);
            day = i;
        else:
            print("Please Enter one of the given numbers");
    # get user input for day of week (all, monday, tuesday, ... sunday)


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 0: # 0 means no filtering
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 0: # 0 means no filtering
        df = df[df['day_of_week'] == day-1] # day - 1 because weekday is 0 based

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june'];
    popular_month = df['month'].mode()[0];
    print("Most Common Month: {}".format(months[popular_month-1].title()));

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    popular_day = df['day_of_week'].mode()[0];
    print("Most Common Day: {}".format(days[popular_day]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_start_station, popular_end_station = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most Common Trip is Start Station: {}, End Station: {}".format(popular_start_station, popular_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration']);
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: {}".format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("Average Travel Time: {}".format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types\n", user_types)

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print("Counts of User Gender\n", user_gender)
    else:
        print("No Available info of User Gender") 

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        df['Birth Year'] = pd.to_numeric(df['Birth Year'])
        earliest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        popular_year = df['Birth Year'].mode()[0]
        print("Earliest Birth Year: {}".format(int(earliest_year)))
        print("Most Recent Birth Year: {}".format(int(latest_year)))
        print("Most Common Birth Year: {}".format(int(popular_year)))
    else:
        print("No Available info of Birth Year")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        rawDataPrompt = True;
        df2 = df.copy() # a copy df for manipulation
        df2.drop(columns= ['month', 'day_of_week', 'hour'], axis= 1, inplace= True);
        start = 0
        end = 5
        while rawDataPrompt:
            c = input("Do you want to show raw data, enter yes or no. \n");
            if c == 'yes':
                print(df2[start:end])
                start += 5
                end += 5
                if df2.shape[0] <= start:
                    print('This is the last bunch of raw data available for you');
                    rawDataPrompt = False;         
            else:
                rawDataPrompt = False;
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
