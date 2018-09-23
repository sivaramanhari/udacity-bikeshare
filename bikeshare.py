#!/usr/bin/env python

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'newyork': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Parmeters:
    -----------
    No arguments expected.

    Returns:
    --------
    city: string
      Name of the city to analyze

    month: string
      Name of the month to filter by, or "all" to apply no month filter

    day: string
      Name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data!")
    city, month, day = '', '', ''
    city_name = {'ch': 'chicago',
                 'ny': 'newyork',
                 'wdc': 'washington'}

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while city != 'newyork' and city != 'chicago' and city != 'washington':
        city = raw_input('''Select city: NewYork[NY], Chicago[CH], Washington[WDC]:\n''')
        city = city.lower()

        # get city names if input is an abbrevation
        if len(city) <= 3:
            try:
                city = city_name[city]
            except KeyError:
                print("Oops you seemed to have entered a wrong choice")

        if city != 'newyork' and city != 'chicago' and city != 'washington':
            print("You did not select from an available option")

    print("You have selected {} City for Analyze".format(city.title()))

    # get user input for month (all, january, february, ..., june)
    while month not in {"all", "january", "febuary",
                        "march", "april", "may", "june"}:
        month = raw_input('''Select a Month: January, Febuary, March, April, May, June or type 'all' to dispaly stats for all months:\n''')
        month = month.lower()

    print("Applied {} month(s) to the filter".format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in {"all", "monday", "tuesday", "wednesday",
                      "thursday", "friday", "saturday", "sunday"}:
        day = raw_input('''Select a day that you want to filter by: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type 'all' to dispaly stats for all days:\n''')
        day = day.lower()

    print("Applied {} day(s) to the filter".format(day.title()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by
    month and day if applicable.

    Parameters:
    -----------
    city: string
        Name of the city to analyze

    month: string
        Name of the month to filter by, or "all" to apply no month filter

    day: string
        Name of the day of week to filter by, or "all" to apply no day filter

    Returns:
    --------
    df: Pandas DataFrame
        It contains city data filtered by month and day
    """

    # get the city csv file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'febuary', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Parameters:
    -----------
    df: Pandas DataFrame
        It contains city data filtered by month and day

    Returns:
    --------
    No return
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'febuary', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print("Most common month: {}".format(months[common_month-1].title()))

    # display the most common day of week
    print("Most common Day: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most Common hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Parameters:
    -----------
    df: Pandas DataFrame
        It contains city data filtered by month and day

    Returns:
    --------
    No return
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commanly used start station: \"{}\""
          .format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commanly used end station: \"{}\""
          .format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    station_stats = df.groupby(['Start Station',
                                'End Station']).size().reset_index()

    station_stats_max_travelled = station_stats[0].max()
    station_stats = station_stats[station_stats[0] == station_stats_max_travelled]

    print("The most frequented travel router is from \"{}\" to \"{}\""
          .format(station_stats.iloc[0]['Start Station'],
                  station_stats.iloc[0]['End Station']))

    print("The route was taken {} times"
          .format(station_stats_max_travelled))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Parameters:
    -----------
    df: Pandas DataFrame
        It contains city data filtered by month and day

    Returns:
    --------
    No return
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['trip_time'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("Total Duration: {}".format(df['trip_time'].sum()))

    # display mean travel time
    print("Mean duration: {}".format(df['trip_time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Parameters:
    -----------
    df: Pandas DataFrame
        It contains city data filtered by month and day

    Returns:
    --------
    No return
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    except KeyError:
        print("Gender data not found for the city you have selected...")

    # Display earliest, most recent, and most common year of birth
    try:
        year_of_birth = df['Birth Year']
        print("Our oldest commuter was born in the year   :{}"
              .format(int(year_of_birth.min())))
        print("Our Yongest commuter was born in the year  :{}"
              .format(int(year_of_birth.max())))
        print("Average birth year of commuters            :{}"
              .format(int(year_of_birth.mode()[0])))
    except KeyError:
        print("Birth Year data not found for the city you have selected...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def dispaly_rawdata(df):
    '''
    Display the raw data from the csv file with respect to the applied filter.

    Parameters:
    -----------
    df: Pandas DataFrame
        It contains city data filtered by month and day

    Returns:
    --------
    No return
    '''

    # Lets default to yes as we want to print the 5 rows when function called
    user_choice = "yes"
    print_rows = 0

    while True:
        print(df[print_rows:print_rows + 5])
        user_choice = raw_input('''Yes[Y] to continue.
                                Press any other key to exit: ''')
        if user_choice.lower() in ("yes", "y"):
            print_rows += 5
        else:
            break


def main():
    '''
    The main method that call all other methods and
    assgin the respective return value.

    Parameters:
    -----------
    No arguments excepted.

    Returns:
    --------
    No return
    '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        user_choice = raw_input('''Would you like to view raw data? Yes[Y] or No[N]\n''')
        dispaly_rawdata(df) if user_choice.lower() in ("yes", "y") else False

        restart = raw_input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
