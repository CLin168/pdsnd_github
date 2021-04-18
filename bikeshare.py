import sys
import time
import pandas as pd
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'satuday', 'sunday']

RAW_COLUMNS = list()
RAW_COLUMN_INDEXES = list()


def choice(prompt, choices, exit_on_int=True):
    """
    Prompts user for input, match input with choices, returns matched input,
    or repeat prompt otherwise. 
    Returns None if exit_on_int is false when user interrupts with control-C
    """

    msg = str(prompt) + ' [' + ', '.join([str(x).title()
                                          for x in choices]) + ']: '

    while True:
        try:
            ret = input(msg).lower()

        except KeyboardInterrupt:
            print('\nUser interrupted, exit')
            if exit_on_int == True:
                sys.exit()
            return None

        # replace multiple spaces in the input string to single space
        # also trim leading and trailing spaces
        ret = ' '.join(ret.split())

        if ret in [str(x).lower() for x in choices]:
            break
        print("[%s] is not a valid choice, please try again" % ret)

    return ret


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

    city = choice('Name of the city to analyze', CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)

    month = choice('Name of the month to analyze', ['all']+MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = choice('Day of the week to analyze', ['all']+DAYS)

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
    print('Loading file of %s' % city.title())
    start_time = time.time()

    df = pd.read_csv(CITY_DATA[city])

    # NB: data contains 'Unnamed: 0' column which has no explained meaning in the
    # project description
    # Remove the 'Unnamed: 0' column since we don't need it for the rest of the project
    if 'Unnamed: 0' in df:
        del df['Unnamed: 0']

    # remember the original column names, this will be used to display the raw data
    global RAW_COLUMNS
    global RAW_COLUMN_INDEXES

    # exclude the 'Unnamed: 0' column name
    RAW_COLUMNS = [c for c in list(df.columns) if c != 'Unnamed: 0']

    RAW_COLUMN_INDEXES = [df.columns.get_loc(
        c) for c in RAW_COLUMNS if c in df]

    # treat rows with any missing data as invalid records
    # remove rows with missing data
    df.dropna(subset=RAW_COLUMNS, inplace=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

    # aggregate Start Stations and End Stations into trips
    # this will be used to find the most popular trip

    print('\nCreating a table of trips by aggregrating start and end stations...\n')
    start_time = time.time()

    df['trip'] = df[['Start Station', 'End Station']].agg('^'.join, axis=1)

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0] - 1
    print("Most common month of travel is", MONTHS[month].title())

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print("Most common day in a week for travel is", day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    print("Most common hour for travel is", hour)

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    print("Most commonly used start station is", start)

    # display most commonly used end station
    end = df['End Station'].mode()[0]
    print("Most comonly used end station is", end)

    # display most frequent combination of start station and end station trip

    trip = df['trip'].mode()[0].split('^')
    print("Most common trip is from", trip[0], "to", trip[1])

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = int(df['Trip Duration'].sum())
    print("Total travel time is %s." % str(dt.timedelta(seconds=total)))

    # display mean travel time
    mean = int(df['Trip Duration'].mean())
    print("Average travel time is %s." % str(dt.timedelta(seconds=mean)))

    # display max travel time
    max = int(df['Trip Duration'].max())
    print("Longest travel time is %s." % str(dt.timedelta(seconds=max)))

    # display min travel time
    min = int(df['Trip Duration'].min())
    print("Shortest travel time is %s." % str(dt.timedelta(seconds=min)))

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    # not all data sets have this column
    if 'Gender' in list(df.columns):
        print("\nCounts of traveler gender:")
        print(df['Gender'].value_counts().to_string())
    else:
        print("\nNo gender data available")

    # Display earliest, most recent, and most common year of birth
    # not all data sets have this column
    if 'Birth Year' in list(df.columns):
        print("\n")
        print("Earliest traveler year of birth is %i." %
              int(df['Birth Year'].min()))
        print("Most recent traveler year of birth is %i." %
              int(df['Birth Year'].max()))
        print("Most common traveler year of birth is %i." %
              int(df['Birth Year'].mode()[0]))
    else:
        print("\nNo traveler birth year data available")

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df, rows=0):
    """interactively display 'rows' rows of raw data."""

    if rows == None or rows <= 0:
        # default to 5 rows of data for each page of display
        rows = 5

    # uncomment next line to set option to display all columns,
    # doing so may ressult in each row being broken into multiple lines

    # pd.set_option('display.max_columns', None)

    start = 0
    end = start + rows
    total = len(df)

    while True:
        res = choice('Do you want to display next ' + str(rows) +
                     ' rows of data', ['yes', 'no'], False)

        if res.lower() != 'yes':
            break
        part = df.iloc[start:end, RAW_COLUMN_INDEXES]
        print(part)
        print("-"*40)
        start = end
        end = start + rows
        if end >= total:
            # start over from first row
            start = 0
            end = start + rows - 1


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = choice('\nWould you like to restart?', ['yes', 'no'])

        if restart.lower() != 'yes':
            print('Goodbye')
            break


if __name__ == "__main__":
    main()
