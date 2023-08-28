#####################################################
# DATA STORY
#####################################################


# This dataset includes information on a company's website as well as statistics about how many users saw
# and clicked on ads, as well as earnings from these interactions.
# There are two separate datasets: Control Group with 'Maximum Bidding' and Test Group with 'Average Bidding'.

# I will apply A/B Testing on These Bidding Methods in order to compare.

# Variables:

# Impression: Number of ad views
# Click: Number of clicks on displayed ads
# Purchase: Number of products purchased after clicking on ads
# Earning: Earnings obtained after the purchase of products from the ads




import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#####################################################
# TASK 1:  ANALYZING THE DATA
#####################################################

# Step 1:  reading the dataset and assigning the control (df_control) and test group (df_test) to separate variables.


df_control = pd.read_excel("2_Measurement_Problems/Week_6/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("2_Measurement_Problems/Week_6/ab_testing.xlsx", sheet_name="Test Group")


# Step 2: Analyzing the control and test group data.

df_control.head()
# Out[1]:
#     Impression      Click  Purchase    Earning
# 0  82529.45927 6090.07732 665.21125 2311.27714
# 1  98050.45193 3382.86179 315.08489 1742.80686
# 2  82696.02355 4167.96575 458.08374 1797.82745
# 3 109914.40040 4910.88224 487.09077 1696.22918
# 4 108457.76263 5987.65581 441.03405 1543.72018


df_test.head()

df_control.info()
df_test.info()

df_control.describe()
# Out[2]:
#         Impression      Click  Purchase    Earning
# count     40.00000   40.00000  40.00000   40.00000
# mean  101711.44907 5100.65737 550.89406 1908.56830
# std    20302.15786 1329.98550 134.10820  302.91778
# min    45475.94296 2189.75316 267.02894 1253.98952
# 25%    85726.69035 4124.30413 470.09553 1685.84720
# 50%    99790.70108 5001.22060 531.20631 1975.16052

df_test.describe()

df_test["diff_label"] = "test"
df_control["diff_label"] = "control"

# Step 3: After the analysis, combining the control and test group data using the concat method.

df_united = pd.concat([df_test, df_control], ignore_index=True)
df_united.head()
# Out[3]:
#     Impression      Click  Purchase    Earning diff_label
# 0 120103.50380 3216.54796 702.16035 1939.61124       test
# 1 134775.94336 3635.08242 834.05429 2929.40582       test
# 2 107806.62079 3057.14356 422.93426 2526.24488       test
# 3 116445.27553 4650.47391 429.03353 2281.42857       test
# 4 145082.51684 5201.38772 749.86044 2781.69752       test

df_united.info()

df_united.describe()
# Out[4]:
#         Impression      Click  Purchase    Earning
# count     80.00000   80.00000  80.00000   80.00000
# mean  111111.93041 4534.10357 566.50008 2211.72952
# std    21623.80775 1272.37607 148.14184  421.70058
# min    45475.94296 1836.62986 267.02894 1253.98952
# 25%    95063.86063 3632.89183 458.13788 1945.71316
# 50%   114037.03500 4321.60283 532.12508 2205.53626
# 75%   124138.65239 5272.61606 679.55760 2541.37752
# max   158605.92048 7959.12507 889.91046 3171.48971

#####################################################
# TASK 2:  Defining the A/B Test Hypothesis
#####################################################

# Step 1: The Hypothesis

"the null hypothesis,H0, claims that there is no significant difference between the means of the two groups (M1 and M2)" \
"the alternative hypothesis,H1, claims that there is a significant difference between the means of the two groups (M1 and M2)"

"H0 : M1 == M2"
"H1 : M1 != M2"

# Step 2: Analyzing the "purchase" averages for the test and control groups.

df_united.groupby("diff_label").agg({"Purchase": "mean"}).reset_index()
# Out[5]:

#   diff_label  Purchase
# 0    control 550.89406
# 1       test 582.10610

#####################################################
# TASK 3: Performing Hypothesis Testing
#####################################################



######################################################
# AB Testing (T-Test)
######################################################


# Step 1: Before testing the hypothesis, checking the assumptions : Normal distribution and homogeneity of variances


# H0:  the data follows a normal distribution.
# H1:  the data does not follow a normal distribution.

test_stat, pvalue = shapiro(df_united.loc[df_united["diff_label"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_united.loc[df_united["diff_label"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



# control group, p-value: 0.5891 > 0.05
#    test group, p-value: 0.1541 > 0.05

# H0 can not be rejected

###################    homogeneity of variances   ##############################
# H0: the variances of all groups are equal.
# H1: the variances of all groups are not equal.

test_stat, pvalue = levene(df_united.loc[df_united["diff_label"] == "control", "Purchase"],
                           df_united.loc[df_united["diff_label"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value: 0.1083 > 0.05
# H0 can not be rejected



# Step 2: Selecting the appropriate test according to Normal distribution and homogeneity of variances

"""
The assumptions are satisfied, hence an independent t-test (parametric test) is performed.

"""

test_stat, pvalue = ttest_ind(df_united.loc[df_united["diff_label"] == "control", "Purchase"],
df_united.loc[df_united["diff_label"] == "test", "Purchase"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value: 0.3493 > 0.05
# Therefore, H0 can not be rejected.


"""
So, There is NO statistically significant difference between the control and test group purchasing averages.
"""


##############################################################
# TASK 4 : Analysis of Results
##############################################################


"""
When the assumption of normality (Shapiro test) and homogeneity of variance (levene test) were examined, p-value values were lower than 0.05.
So, Parametric test (t-test) was applied.
"""

# A little advice for the customer :))

"""
Although there is no statistically significant difference between the purchasing averages of the control and test groups,
these results do not necessarily indicate that they are unimportant. 
By increasing/changing our sample size -control and test group-
and/or increasing the application time .. at least 6 months .., we can detect a statistically significant difference.
"""
