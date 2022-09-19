import time
import pandas as pd
import numpy as np

CITY_DATA = { "chicago": "chicago.csv",
              "nyc": "new_york_city.csv",
              "washington": "washington.csv"}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("\nHello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("\nWhich city would you like to explore? Chicago, NYC or \
Washington? \n").lower()
        if city in ["chicago", "nyc","washington"]:
            break
        else:
            print("\nPlease enter a valid city (Chicago, NYC or Washington)")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nFor which month between January and June? Please type \
'all' for no month filter: \n").lower()
        if month in ["january","february","march","april","may","june",\
         "all"]:
            break
        else:
            print("Please select a valid month (January to June)")

    # get user input for day of week (all, monday,  tuesday, ... sunday)
    while True:
        day = input("\nFor which weekday? Please type 'all' for no day filter:\
 \n").lower()
        if day in ["monday","tuesday","wednesday","thursday","friday",\
        "saturday","sunday","all"]:
            break
        else:
            print("Please select a valid weekday")

    print("\nExcellent! You have chosen the city {}, month {} and weekday {}.".\
format(city.upper(),month.upper(),day.upper()))

    check_input()

    return city, month, day


def check_input():

    """
    Check user input to avoid invalid cities, months or weekdays
    Displays a message with error message in case of invalid input
    Asks for new input
    """

    while True:
        check_input = input("\nIs it correct? Enter 'yes' to continue or any \
other character to input again.\n")
        if check_input.lower() != "yes":
            get_filters()
        else:
            print("-"*40)
        break


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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]


    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    popular_month = df["month"].mode()[0]

    # display the most common day of week
    popular_weekday = df["day_of_week"].mode()[0]

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]

    print("\nTime statistics: \n")
    print("The most common travel month is {}.\nThe most common weekday is {}.\n\
The most common start hour is {}.".format(popular_month,popular_weekday,\
popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    popular_startst = df["Start Station"].mode()[0]

    # display most commonly used end station
    popular_endst = df["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    df["station_comb"] = "start at " + df["Start Station"] + " and end \
at " + df["End Station"]
    popular_comb = df["station_comb"].mode()[0]

    print("\nStation statistics: \n")
    print("The most commonly used start station is {}.\nThe most commonly used\
end station is {}.\nThe most frequent start/end combination is {}.".format\
(popular_startst,popular_endst,popular_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    travel_time = df["End Time"] - df["Start Time"]
    total_travel_time = travel_time.sum()

    # display mean travel time
    mean_time = travel_time.mean().round("1s")

    print("\nTrip duration statistics:\n")
    print("The total travel time is {}.\nThe average travel time is {}.".\
        format(total_travel_time,mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("-"*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types

    user_types = df["User Type"].value_counts()
    print("\nUser statistics: \n")
    print("The user types counting results are: \n{}.\n".format([user_types]))

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # gender and birthyear not avalable for washington

    if city != "washington":
        gender_types = df["Gender"].value_counts()
        earliest_birthyear = int(df["Birth Year"].min())
        recent_birthyear = int(df["Birth Year"].max())
        most_common_birthyear = int(df["Birth Year"].mode()[0])
        print("The gender counting results are: \n{}.\n".format([gender_types]))
        print("The earliest birthyear is {}.\nThe most recent birthyear is {}.\n\
The most common birthyear is {}.".format(earliest_birthyear,recent_birthyear,\
most_common_birthyear))

    else:
        print("Gender and birthyear information are not available for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("-"*40)


def row_entries(df):

    """Ask user if he/she wants to check detailed information (row entries)"""

    raw_data = input("\nWould you like to check the first 5 lines of raw data? \
Please enter 'yes' or any other character to cancel: ").lower()

    start_line = 0

    while True:
        if raw_data == "yes":
            print(df.iloc[start_line:start_line+5])
            start_line += 5
        else:
            break

        additional_rows = input("\nWould you like to check the next 5 lines of \
raw data? Please enter 'yes' or any other character to cancel: ").lower()
        if additional_rows != "yes":
            break

        print("-"*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        row_entries(df)

        restart = input("\nEnter 'yes' to restart or any other character to \
finish the program.\n")
        if restart.lower() != "yes":
            break

if __name__ == "__main__":
	main()
