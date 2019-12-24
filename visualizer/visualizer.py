import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters

import config

register_matplotlib_converters()
from matplotlib import rcParams, ticker
from matplotlib.dates import num2date

rcParams.update({'figure.autolayout': True})


class Visualizer:
    '''
    This class provides methods for generating visual report for the agreed csv file. This methods will begin with
    generate_***
    '''

    # Constants
    DATE = "date"
    USAGE = "usage"
    AMOUNT = "amount"
    DEBITOR = "debitor"
    WEEKDAY = "weekday"

    WEEKDAY_COLOR = {
        'Monday': '#00ffff',
        'Tuesday': '#00bbff',
        'Wednesday': '#0077ff',
        'Thursday': '#0033ff',
        'Friday': '#0000ff',
        'Saturday': '#ff0000',
        'Sunday': '#8a0000'}

    def __init__(self, sales, save_dir):
        self.save_dir = save_dir
        print("Save results in ", self.save_dir)

        # methods for generating reports will use this
        sales = self.__preprocess(sales)
        self.__start_date = sales[self.DATE].min()
        self.__end_date = sales[self.DATE].max()
        self.__spendings = self.__get_spending(sales)
        self.__earnings = self.__get_earnings(sales)
        self.__str_start_to_end_date = f"{self.__start_date.strftime(config.DATE_FORMAT)} to {self.__end_date.strftime(config.DATE_FORMAT)}"

    def __preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Preprocess the data.

        - Sort by date
        - Add column 'weekday' and assign weekday corresponding to the date

        :param df: Raw data frame
        :return: Preprocessed data frame
        '''

        # sort by date and reset index for hte new order
        df[self.DATE] = pd.to_datetime(df[self.DATE], format=config.DATE_FORMAT)
        df = df.sort_values(by=[self.DATE])
        df = df.reset_index(drop=True)

        # create new column and assign weekday
        df[self.WEEKDAY] = df[self.DATE].dt.day_name()

        return df

    def __get_spending(self, sales: pd.DataFrame) -> pd.DataFrame:
        '''
        Get spending with absolute numbers

        :param sales:
        :return:
        '''

        spendings = pd.DataFrame(data=sales[sales[self.AMOUNT] < 0])
        spendings[self.AMOUNT] = spendings[self.AMOUNT].abs()

        return spendings

    def __get_earnings(self, sales: pd.DataFrame) -> pd.DataFrame:
        '''
        Get earnings with absolute numbers

        :param sales:
        :return:
        '''
        return pd.DataFrame(data=sales[sales[self.AMOUNT] > 0])

    def __generate_bins_amount(self, df: pd.DataFrame, title: str, bins: int = 20) -> None:
        """
        Generate a bar chart with spendings bins.

        :return:
        """

        # deep copy to no mess up with the original data
        df = df.copy()

        # style of plot
        plt.figure(figsize=(8, 5))
        plt.title(title)
        plt.xticks(rotation=90)

        # set bin color
        bin_colors = ["#00" + hex(x)[2:4].zfill(2) + "ff" for x in np.linspace(255, 0, bins, dtype=int)]
        # set bin x-ticks
        spending_bins = pd.cut(df[self.AMOUNT], bins, precision=0).value_counts(sort=False)
        spending_bins.index = [str((x.right + x.left) / 2) + ' \u00B1 ' + str((x.right - x.left) / 2) for x in
                               spending_bins.index]

        # generate bins
        for i, (r, amount) in enumerate(spending_bins.iteritems()):
            plt.bar(str(r), amount, width=1, color=bin_colors[i])

        # save
        plt.savefig(os.path.join(self.save_dir, title))

    def __generate_timeline(self, df: pd.DataFrame, title: str) -> None:
        """
        Generate a timeline chart where the weekdays are color coded.

        :return:
        """

        # deep copy to no mess up with the original data
        df = df.copy()

        # init plot
        plt.figure(figsize=(20, 5))
        ax = plt.axes()
        plt.title(title)

        # xticks
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(MyDateFormatter(self.__start_date, self.__end_date))

        # timeline plot
        cum = df[self.AMOUNT].cumsum()
        plt.plot_date(df[self.DATE], cum, color='black')

        # weekday marking plot
        days_in_month = pd.date_range(start=self.__start_date, end=self.__end_date)
        for i, d in enumerate(days_in_month):
            plt.bar(days_in_month[i], cum.iloc[-1],
                    width=1,
                    color=self.WEEKDAY_COLOR[d.day_name()], alpha=0.5)

        # save
        plt.savefig(os.path.join(self.save_dir, title))

    def __generate_bins_weekdays(self, df: pd.DataFrame, title: str) -> None:
        '''
        Genarate a bar plot with weekdays as bins.

        :return:
        '''

        # deep copy to no mess up with the original data
        df = df.copy()

        # inti plot
        plt.figure(figsize=(8, 5))
        plt.title(title)
        plt.xticks(rotation=90)

        # Making categorical bins to later sum up upon
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['weekday'] = pd.Categorical(df['weekday'], categories=days)

        # making bins
        spendings_in_week = df[['weekday', 'amount']].groupby('weekday').sum()

        # plotting bins
        for week_day, e in spendings_in_week.iterrows():
            plt.bar(week_day, e[self.AMOUNT],
                    width=1,
                    color=self.WEEKDAY_COLOR[week_day], alpha=0.5)

        # save
        plt.savefig(os.path.join(self.save_dir, title))

    def generate_spending_bins_amount(self):
        self.__generate_bins_amount(self.__spendings,
                                    f"Generated spending bins amount ({self.__str_start_to_end_date})")

    def generate_spending_bins_weekdays(self):
        self.__generate_bins_weekdays(self.__spendings,
                                      f"Generated spending bins weekday ({self.__str_start_to_end_date})")

    def generate_spending_timeline(self):
        self.__generate_timeline(self.__spendings,
                                 f"Generated spending timeline ({self.__str_start_to_end_date})")

    def generate_earning_bins_amount(self):
        self.__generate_bins_amount(self.__earnings,
                                    f"Generated earning bins amount ({self.__str_start_to_end_date})")

    def generate_earning_bins_weekdays(self):
        self.__generate_bins_weekdays(self.__earnings,
                                      f"Generated earning bins weekday ({self.__str_start_to_end_date})")

    def generate_earning_timeline(self):
        self.__generate_timeline(self.__earnings,
                                 f"Generated earning timeline ({self.__str_start_to_end_date})")


class MyDateFormatter(ticker.Formatter):
    """
    Custom ticker formatter

    Show month and day for start and end dates
    Show month and day also for the first day of the month
    For every other dates show only the day
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __call__(self, x, pos=0):
        date = num2date(x)

        if date.date() == self.start_date.date() or date.date() == self.end_date.date() or date.day == 1:
            r = date.strftime("%d.%m")
        else:
            r = date.strftime("%d")

        return r
