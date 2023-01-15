# from newsapi import NewApiClient
from newsapi.newsapi_client import NewsApiClient
import pycountry

# you have to get your api key from newapi.com and then paste it below
newsapi = NewsApiClient(api_key='198d457ed2874e37a151f7d8aae41c52')


def NewsHeadlines(con, option):

    with open("news.txt", "w") as f:
        f.write("")

    # now we will take name of country from user as input
    input_country = con
    input_countries = [f'{input_country.strip()}']
    countries = {}

    # iterate over all the countries in
    # the world using pycountry module
    for country in pycountry.countries:

        # and store the unique code of each country
        # in the dictionary along with it's full name
        countries[country.name] = country.alpha_2

    # now we will check that the entered country name is
    # valid or invalid using the unique code
    codes = [countries.get(country.title(), 'Unknown code')
             for country in input_countries]

    # now we have to display all the categories from which user will
    # decide and enter the name of that category
    # option = input("Which category are you interested in?\n1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n\nEnter here: ")
    # now we will fetch the new according to the choice of the user
    top_headlines = newsapi.get_top_headlines(

        # getting top headlines from all the news channels
        category=f'{option.lower()}', language='en', country=f'{codes[0].lower()}')

    # fetch the top news inder that category
    Headlines = top_headlines['articles']
    # now we will display the that news with a good readability for user
    i = 1
    if Headlines:
        for articles in Headlines:

            if i <= 5:

                b = articles['title'][::-1].index("-")

                if "news" in (articles['title'][-b+1:]).lower():
                    with open("news.txt", "a") as f:
                        f.write(
                            f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.\n\n")

                else:
                    with open("news.txt", "a") as f:
                        f.write(
                            f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.\n\n")
                i += 1
    else:
        print(
            f"Sorry no articles found for {input_country}, Something Wrong!!!")
