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
    while True:
        city=input("Which City You Like To See (Chicago,New york city,Washington) : ")
        if city.lower() in ['chicago','new york city','washington']:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month=input("Which Month You Want To See (January, February, March, April, May, or June) (All : for all months) : ")
        if month.lower() in ['all','january', 'february', 'march', 'april', 'may', 'june']:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Which Day You Want To See (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday) (All : for all days) : ")
        if day.lower() in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most Common Month is : {}".format(str(df['month'].mode()[0])))

    # display the most common day of week
    print("Most Common Day is   : {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most Common Hour is  : {}".format(str(df['hour'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station=df['Start Station'].mode()[0]
    most_start_station_counts=df['Start Station'].value_counts()
    print("Most Commonly Used Start Station is : {} which is counted : {}".format(most_common_start_station,str(most_start_station_counts[most_common_start_station])))

    # display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    most_end_station_counts=df['End Station'].value_counts()
    print("Most Commonly Used End Station is   : {} which is counted : {}".format(most_common_end_station,str(most_end_station_counts[most_common_end_station])))

    # display most frequent combination of start station and end station trip
    print("Most Frequent Combination Of Start Station And End Station Trip : ")
    df['combinations']=df['Start Station']+" to "+df["End Station"]
    most_frequent_combination=df['combinations'].mode()[0]
    print(most_frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("Total Travel Time is : {}".format(str(total_travel_time)))

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("Mean Travel Time is  : {}".format(str(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types=df['User Type'].value_counts()
    print("Subscriber Counts : {} ".format(counts_of_user_types['Subscriber']))
    print("Customer   Counts : {} ".format(counts_of_user_types['Customer']))
    # Display counts of gender
    try:
        counts_of_gender=df['Gender'].value_counts() # type of pandas Series
        print("Male   Counts : {} ".format(counts_of_gender['Male']))
        print("Female Counts : {} ".format(counts_of_gender['Female']))

    # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth=df['Birth Year'].min()
        most_recent_year_of_birth=df['Birth Year'].max()
        most_common_year_of_birth=df['Birth Year'].mode()[0]
        print("Earliest Year Of Birth is : {}".format(str(earliest_year_of_birth)))
        print("Most Recent Year Of Birth is : {}".format(str(most_recent_year_of_birth)))
        print("Most Common Year Of Birth is : {}".format(str(most_common_year_of_birth)))
    except:
        print("Gender and Birth Year are not available for this City ")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    display=input(' Do you want to see the first 5 rows of data? (yes or no)')
    start_loc=0
    end_loc=5
    while display.lower()=='yes':
        number_of_rows=df.shape[0]
        if end_loc>number_of_rows:
            print(df.iloc[start_loc:])
            print("**********End Of Rows**********")
            break
        else:
            print(df.iloc[start_loc:end_loc])
            start_loc+=5
            end_loc+=5
            display=input(' Do you want to see the next 5 rows of data? (yes or no)')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
