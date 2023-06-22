import pandas as pd

def get_rich_percentage(salary_series):
    salary_counts = salary_series.value_counts()
    if salary_counts.get(">50K"):
        result = (salary_counts.get(">50K")/salary_counts.sum()) * 100
    else:
        result = 0
    return result


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    print(df)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.race.value_counts()

    # What is the average age of men?
    mean = df.groupby('sex', as_index=False).age.mean()
    average_age_men = mean.iloc[1, 1].round(decimals=1)

    # What is the percentage of people who have a Bachelor's degree?
    # Total number of bachelors degrees
    bachelors_count = df.education.value_counts().loc['Bachelors']
    # Total number of education degrees
    education_count = df.education.value_counts().sum()
  
    percentage_bachelors = ((bachelors_count / education_count) * 100).round(decimals=1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    people = df.groupby('education').salary.value_counts()
    
    sum_morethan_50k= people.loc[['Bachelors', 'Masters', 'Doctorate'], '>50K'].sum()
    sum_lessthan_50k = people.loc[['Bachelors', 'Masters', 'Doctorate'], '<=50K'].sum()
    sum_morethan_lessthan = sum_morethan_50k + sum_lessthan_50k
    percentage_higher = ((sum_morethan_50k / sum_morethan_lessthan) * 100).round(decimals=1)
      # What percentage of people without advanced education make more than 50K?
    people1 = people.drop(['Bachelors', 'Doctorate', 'Masters'])
    
    sum_lower_morethan50k = people1.loc[:, '>50K'].sum()
    sum_lower_lessthan50k = people1.loc[:, '<=50K'].sum()
    total_sumlower = sum_lower_morethan50k + sum_lower_lessthan50k
    percentage_lower = ((sum_lower_morethan50k / total_sumlower) * 100).round(decimals=1)

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = sum_morethan_lessthan
    lower_education = total_sumlower

    # percentage with salary >50K
    higher_education_rich = percentage_higher
    lower_education_rich = percentage_lower

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    time = df.groupby('hours-per-week').salary.value_counts()
    min_earnabove_50k = time.loc[1, '>50K']
    
    num_min_workers = time.loc[1, ['>50K', '<=50K']].sum()

    rich_percentage = ((min_earnabove_50k / num_min_workers) * 100).round(decimals=1)

    # What country has the highest percentage of people that earn >50K?
    by_country = df.groupby("native-country")
    rich_percentage_by_country = by_country.apply(lambda group: get_rich_percentage(group["salary"])).sort_values(ascending=False)
    highest_earning_country = rich_percentage_by_country.idxmax()
    highest_earning_country_percentage = rich_percentage_by_country[highest_earning_country]
    highest_earning_country_percentage = round(highest_earning_country_percentage, 1)
    # Identify the most popular occupation for those who earn >50K in India.
    salary_filter = df["salary"] == ">50K"
    country_filter = df["native-country"] == "India"
    richer_indians = df[(country_filter)&(salary_filter)]
    indian_occupations = richer_indians.groupby("occupation").size()
    top_IN_occupation = indian_occupations.idxmax()


    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
