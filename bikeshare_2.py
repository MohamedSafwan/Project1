import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
year_months = ["January", "February", "March", "April", "May", "June", "All"]
week_days = [
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "All",
]
The_city = ""
The_month = ""
The_day = ""


def get_filters():
    global The_city
    global The_month
    global The_day
    """
    Asks user to specify a city, month, and day to analyze.
    

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Pleas choose one of these cities "Chicago, New York City, Washington"?==> '
        ).lower()
        if city not in CITY_DATA:
            print("\n\t\t!!Warning!!\nThe city you entered is not a valid city name!\n")
            continue
        else:
            print("\nThis is clear that {} is your selected city.".format(city.title()))
            The_city = city
            break
        # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            '\nWhich month do you like to filter the data by:\nJanuary, February, March, April, May, June, or type "all" to apply no month filter==> '
        ).title()
        if month not in year_months:
            print("\n!!Warning!!\nThe month you entered is not a valid month name!")
            continue
        else:
            The_month = month
            if month != "All":
                print("\nThe data will be filtered by {}.".format(month))
            else:
                print("\nThe data will not be filtered by a specific month.")
            break
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            '\nWhich day do you like to filter the data by:\nSaturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or type "all" to apply no day filter==> '
        ).title()
        if day not in week_days:
            print("\n!!Warning!!\nThe day you entered is not a valid day name!")
            continue
        else:
            if day != "All":
                print("\nThe data will be filtered by {}.".format(day))
            else:
                print("\nThe data will not be filtered by a specific day.")
            The_day = day
            break

    print("-" * 40)
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
    df = pd.read_csv(CITY_DATA[city], parse_dates=(["Start Time", "End Time"]))

    # extract month and day of week from Start Time and create new columns
    df["month"], df["day_of_week"] = (
        df["Start Time"].dt.month_name(),
        df["Start Time"].dt.day_name(),
    )

    # filter by month if applicable
    if month != "All":
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "All":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    # display the most common month
    if The_month == "All":
        common_month = df["month"].mode()[0]
        print("The most common month is {}.".format(common_month))

    # display the most common day of week
    if The_day == "All":
        common_day = df["day_of_week"].mode()[0]
        print("The most common day is {}.".format(common_day))

    # display the most common start hour
    df["start_hour"] = df["Start Time"].dt.hour
    common_hour = df["start_hour"].mode()[0]
    print("The most common hour is {}:00.".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    # Display most commonly used start station
    common_start_station2 = df["Start Station"].mode()[0]
    count_start = df["Start Station"][
        df["Start Station"] == common_start_station2
    ].count()
    print(
        "The most common start staion is {} with {} frequent repetition".format(
            common_start_station2, count_start
        )
    )

    #######################
    """Another code giving the same results"
     common_start_station = df['Start Station'].value_counts()
    the_station = common_start_station[common_start_station.values == max(common_start_station.values)]
    print('The most common start staion is {}  with {} frequent repetition'.format(the_station.index, the_station.values))
    """
    #######################

    # Display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    count_end = df["End Station"][df["End Station"] == common_end_station].count()
    print(
        "The most common end staion is {} with {} frequent repetition".format(
            common_end_station, count_end
        )
    )

    # Display most frequent combination of start station and end station trip
    df["common_start_end_station"] = df["Start Station"] + " and " + df["End Station"]
    common_start_end_station = df["common_start_end_station"].mode()[0]
    print(
        "The most common start and end staion combination is {}".format(
            common_start_end_station
        )
    )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("The total travel time is {} hour".format(df["Trip Duration"].sum() / 3600))

    # display mean travel time
    print("The mean travel time is {} minute".format(df["Trip Duration"].mean() / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    global The_city
    """Displays statistics on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print(df["User Type"].value_counts())

    # Display the analysis of gender and year of birth only for Chicago and New York City
    if The_city == "chicago" or The_city == "new york city":
        # Display counts of gender
        gender_counts = df["Gender"].value_counts()
        print(
            "\nThe number of {}s is {} person.".format(
                gender_counts.index[0].lower(), gender_counts.values[0]
            )
        )
        print(
            "The number of {}s is {} person.".format(
                gender_counts.index[1].lower(), gender_counts.values[1]
            )
        )
        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        recent_year = int(df["Birth Year"].max())
        common_year = int(df["Birth Year"].mode())
        print(
            "\nThe earliest year of birth is: {}.\nThe most recent year of birth is: {}.\nThe most common year of birth is: {}.".format(
                earliest_year, recent_year, common_year
            )
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


# A funtion to ask the user for displaying raw data
def raw_data(df):
    i = 0
    while True:
        check = input("Would you like to see raw data? [Yes/No] ").title()
        if check == "Yes":
            print(df.iloc[i:i+5,:])
            i += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #time_stats(df)
        #station_stats(df)
        #trip_duration_stats(df)
        #user_stats(df)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
