#!/bin/python3

import math
import os
import random
import re
import sys


def get_lower_price_day(stockData, calculated_days, day):
    """
    For any given day this function will find the previous day with
    stock price lower than stock price for the given day.
    This function executes recursively finding lower stock prices
    for all days prior to the given day and saves the results in the
    calculated_days array

    :param stockData: An array of stock prices where the array index
    represents days values represent prices
    :param calculated_days: An array where the result will be saved
    :param day: day being queried for
    :return: An integer representing the previous day with lower
    stock price than stock price of day or -1 if not available.
    """

    # Base case
    if day == 0:
        calculated_days[day] = -1
        return -1

    last_day = day - 1

    # compare last_day stock price with stock price for day
    while last_day > -1 and stockData[day] <= stockData[last_day]:

        # set last_day to day with price lower than the last_day
        if calculated_days[last_day] != float("inf"):
            # has been previously calculated
            last_day = calculated_days[last_day]
        else:
            # calculate
            last_day = get_lower_price_day(
                stockData, calculated_days, last_day)

    # Save the last_day with price lower than day
    calculated_days[day] = last_day

    if last_day > -1 and calculated_days[last_day] == float("inf"):
        # Continue calculating for remaining uncalculated days
        get_lower_price_day(stockData, calculated_days, last_day)

    # return the last_day with price lower than day
    return last_day


def get_lower_price_day_iterative(stockData, calculated_days):
    """
    For all days in stockData this function will find the previous day
    with lower stock price and saves the results in the
    calculated_days array.
    This function creates a virtual stack to mimic the behaviour of the
    recursive running function get_lower_price_day.

    :param stockData: An array of stock prices where the array index
    represents days values represent prices
    :param calculated_days: An array where the result will be saved
    """

    # add last day to be compared with the day before to virtual stack
    stack = [(len(stockData) - 1, len(stockData) - 2)]

    # keep executing on days in virtual stack
    while stack:
        day, day_being_compared = stack.pop()

        # base case
        if day == 0:
            calculated_days[day] = -1
            continue

        previous_low_price_day = calculated_days[day_being_compared]
        if previous_low_price_day == float('inf'):
            stack.append((day, day_being_compared))
            stack.append((day_being_compared, day_being_compared - 1))
            continue

        if day_being_compared > -1 and\
                stockData[day] <= stockData[day_being_compared]:
            if calculated_days[day_being_compared] != float('inf'):
                stack.append(
                    (day, calculated_days[day_being_compared])
                )
            else:
                stack.append((day, previous_low_price_day))
                stack.append(
                    (previous_low_price_day, previous_low_price_day-1)
                )
            continue

        calculated_days[day] = day_being_compared


def get_closer_low_price_day(previous_lower_price_days,
                             following_lower_price_days, q):
    """
    Compares which day is closer to the day being queried; the following day with a price
    drop or the previous day with a lower price.

    :param previous_lower_price_days: An array of n integers, where the value of each
    element previous_lower_price_days[i] is the day previous to i with price a lower
    stock price.
    :param following_lower_price_days: An array of n integers, where the value of each
    element following_lower_price_days[i] is the day after i with price a lower
    stock price.
    :param q: An integer q representing the day being queired
    (where 0 <= q < len(previous_lower_price_days)) .
    :return: An integer representing the day closest to q with a lower stock price or -1
    if no day exists.
    """

    if q >= len(previous_lower_price_days):
        return -1

    previous_low_price_day = previous_lower_price_days[q]
    follwing_low_price_day = following_lower_price_days[q]

    if follwing_low_price_day == -1:
        return previous_low_price_day

    if previous_low_price_day == -1:
        return follwing_low_price_day

    days_from_previous_day = abs(q - previous_low_price_day)
    days_from_following_day = abs(q - follwing_low_price_day)
    if days_from_following_day < days_from_previous_day:
        return follwing_low_price_day
    return previous_low_price_day


def predictAnswer(stockData, queries):

    # initialize array for previous low price days
    previous_lower_price_days = [float('inf') for i in
                                 range(len(stockData))]

    # initialize array for following low price days
    following_lower_price_days = [float('inf') for i in
                                  range(len(stockData))]

    # calculate previous low price days for all days
    get_lower_price_day_iterative(
        stockData,
        previous_lower_price_days
    )

    # reverse stockData order
    reversed_stock = stockData.copy()
    reversed_stock.reverse()

    # calculate following low price days for all days
    get_lower_price_day_iterative(
        reversed_stock,
        following_lower_price_days
    )

    # reorder following low price days array
    following_lower_price_days.reverse()
    following_lower_price_days = [
        len(stockData) - i - 1 if i != -1 else i for i in
        following_lower_price_days]

    # Start executing queries and save results to array
    results = []
    for q in queries:
        result = get_closer_low_price_day(
            previous_lower_price_days,
            following_lower_price_days,
            q - 1
        )
        result = result + 1 if result > -1 else result
        results.append(result)
    return results


if __name__ == '__main__':
    module_path = os.path.dirname(os.path.realpath(__file__))
    fptr = open(os.path.join(module_path, 'output_file'), 'w')

    stockData_count = int(input().strip())

    stockData = []

    for _ in range(stockData_count):
        stockData_item = int(input().strip())
        stockData.append(stockData_item)

    queries_count = int(input().strip())

    queries = []

    for _ in range(queries_count):
        queries_item = int(input().strip())
        queries.append(queries_item)

    result = predictAnswer(stockData, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()

