#!/usr/bin/env python
# coding: utf-8

# In[123]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import os
import datetime as dt


# In[124]:


customer = pd.read_csv("D:\Analytics labs 2021\PYTHON\Python Foundation Case Study 2 - Credit Card Case Study\Customer Acqusition.csv")


# In[125]:


Repayment = pd.read_csv("D:\Analytics labs 2021\PYTHON\Python Foundation Case Study 2 - Credit Card Case Study\Repayment.csv")


# In[126]:


spend = pd.read_csv("D:\Analytics labs 2021\PYTHON\Python Foundation Case Study 2 - Credit Card Case Study\spend.csv")


# In[127]:


customer.head()


# In[128]:


customer.dtypes


# In[129]:


customer.isnull().sum()


# In[137]:


spend.head()


# In[138]:


spend.dtypes


# In[139]:


spend.isnull().sum()


# In[140]:


Repayment.head()


# In[141]:


Repayment.dtypes


# In[143]:


Repayment.isnull().sum()


# In[144]:


Repayment.drop(columns='Unnamed: 4',inplace=True)


# In[145]:


Repayment.head()


# In[146]:


Repayment.dropna(inplace=True)


# In[147]:


Repayment.isnull().sum()


# In[148]:


Repayment


# ### 1. In the above dataset,

# #### a. In case age is less than 18, replace it with mean of age values.

# In[149]:


mean_real = customer["Age"].mean()


# In[150]:


mean_real


# In[151]:


customer.loc[customer["Age"] < 18,"Age"] = customer["Age"].mean()


# In[152]:


mean_new = customer["Age"].mean()


# In[153]:


mean_new


# #### b. In case spend amount is more than the limit, replace it with 50% of that customer’s limit. 
# #### (customer’s limit provided in acquisition table is the per transaction limit on his card)

# In[154]:


customer.head()


# In[155]:


spend.head()


# In[156]:


# inner join on 'Customer'

customer_spend = pd.merge(left=customer,right=spend,on="Customer",how="inner")
customer_spend.head()


# In[157]:


# finding customers who spend more than their limit

customer_spend[customer_spend["Amount"] > customer_spend['Limit']]


# In[158]:


# replacing with 50% of that customer’s limit

customer_spend.loc[customer_spend["Amount"] > customer_spend["Limit"],"Amount"] = (50 * customer_spend["Limit"]).div(100)


# In[159]:


customer_spend.head()


# #### c. Incase the repayment amount is more than the limit, replace the repayment with the limit.

# In[160]:


Repayment.head()


# In[161]:


# inner join on 'customer'

customer_Repayment = pd.merge(left=Repayment,right=customer,on="Customer",how="inner")


# In[162]:


customer_Repayment


# In[163]:


# finding customers with repayment more than limit

customer_Repayment[customer_Repayment["Amount"] > customer_Repayment["Limit"]]


# In[176]:


# replacing with limit

customer_Repayment.loc[customer_Repayment["Amount"] > customer_Repayment["Limit"],"Amount"] 


# In[177]:


customer_Repayment


# ### 2. From the above dataset create the following summaries:

# #### a. How many distinct customers exist?

# In[178]:


distinct_customers = customer["Customer"].nunique()


# In[179]:


distinct_customers


# #### b. How many distinct categories exist?

# In[180]:


customer["Segment"].value_counts()


# In[185]:


plt.figure(figsize=(8,6))
sns.countplot('Segment',data=customer)
plt.show()


# In[188]:


print("We can see from the countplot that number of distinct categories are 5")


# #### c. What is the average monthly spend by customers?

# In[189]:


spend.head()


# In[190]:


# convert month to datetime

spend['Month'] = pd.to_datetime(spend['Month'])


# In[191]:


spend['Month'].dtypes


# In[192]:


spend.head()


# In[194]:


# splitting month and year  
spend['Months'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
spend['Year'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[196]:


spend


# In[201]:


# grouping by year and month with average

spend_new= round(spend.groupby(['Year','Month']).mean(),2)


# In[202]:


spend_new


# #### d. What is the average monthly repayment by customers?

# In[203]:


Repayment.dtypes


# In[204]:


Repayment["Month"] = pd.to_datetime(Repayment["Month"])


# In[205]:


Repayment["Month"].dtypes


# In[206]:


# splitting month and year from date

Repayment['Months'] = Repayment ['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
Repayment['Year'] = Repayment['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[208]:


Repayment


# In[213]:


Repayment_new= round(Repayment.groupby(['Year','Months']).mean(),2)


# In[214]:


Repayment_new


# #### e. If the monthly rate of interest is 2.9%, what is the profit for the bank for each month? 
# ####     (Profit is defined as interest earned on Monthly Profit. Monthly Profit = Monthly repayment 
# ####     –  Monthly spend. Interest is earned only on positive profits and not on negative amounts)

# In[221]:


# merging all dataframes

customerAll = pd.merge(left=customer_spend,right=Repayment,on="Customer",how="inner")


# In[222]:


customerAll


# In[223]:


#reanming amount_x as spend_amount and amount_y as repay_amount

customerAll.rename(columns={"Amount_x":"Spend_Amount","Amount_y":"Repayment_Amount"},inplace=True)


# In[224]:


customerAll.head()


# In[225]:


# getting spend and repay data on a monthly and yearly basis

cust_data = customerAll.groupby(["Year","Months"])['Spend_Amount','Repayment_Amount'].sum()


# In[226]:


cust_data


# In[227]:


# profit = Monthly repayment – Monthly spend.

cust_data['Monthly Profit'] = cust_data['Repayment_Amount'] - cust_data['Spend_Amount']


# In[228]:


cust_data


# In[229]:


# checking negative profit

(cust_data['Monthly Profit']<0).sum()


# In[230]:


cust_data['Interest Earned'] = (2.9* cust_data ['Monthly Profit'])/100


# In[231]:


cust_data


# #### f. What are the top 5 product types?

# In[233]:


spend['Type'].value_counts().head()


# #### g. Which city is having maximum spend?

# In[234]:


customer_spend.groupby("City")["Amount"].sum().sort_values(ascending=False)


# In[235]:


## Cochin has the maximum spend


# #### h. Which age group is spending more money?

# In[236]:


customer_spend


# In[237]:


customer_spend['Age'].max()


# In[238]:


customer_spend['Age'].min()


# In[239]:


# creating a column age group

customer_spend["Age Group"] =  pd.cut(customer_spend["Age"],
                                      bins = np.arange(18,88,8),
                                      labels = ["18-26","26-34", "34-42" ,"42-50" ,"50-58","58-66","66-74","74-82"],
                                      include_lowest = True
                                     )


# In[240]:


customer_spend


# In[241]:


customer_spend.groupby("Age Group")['Amount'].sum().sort_values(ascending=False)


# In[242]:


## age group 42-50 spend the most


# #### i. Who are the top 10 customers in terms of repayment?

# In[243]:


# sorting in descending order

customer_repay.groupby("Customer")[["Amount"]].sum().sort_values(by="Amount",ascending=False).head(10)


# ### 3. Calculate the city wise spend on each product on yearly basis. Also include a graphical representation for the same.

# In[244]:


customer_spend.head()


# In[245]:


# month to datetime

customer_spend["Month"] = pd.to_datetime(customer_spend["Month"])


# In[246]:


# since we need yearly spend,creating a new year column and extracting the year 

customer_spend['Year'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[247]:


customer_spend.head(10)


# In[248]:


# we need a pivot table for better view

customer_spend_pivot = pd.pivot_table(data = customer_spend,
                                      index=["City","Year"],
                                      columns='Product',
                                      aggfunc="sum",
                                      values="Amount"
                                     )


# In[249]:


customer_spend_pivot


# In[250]:


# grphical representation

customer_spend_pivot.plot(kind="bar",figsize=(20,10),width=1)
plt.ylabel("Spend Amount")
plt.title("Amount spend by year and city")
plt.show()


# ### 4. Create graphs for

# #### a. Monthly comparison of total spends, city wise

# In[252]:


customer_spend.dtypes


# In[87]:


customer_spend.head()


# In[253]:


customer_spend.isnull().sum()


# In[254]:


customer_spend.head()


# In[255]:


# extracting month and creating a column

customer_spend['Monthly'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[256]:


customer_spend.head()


# In[257]:


#grouping data based on "Monthly" and "City" columns

month_city = customer_spend.groupby(["Monthly","City"])[["Amount"]].sum().sort_index().reset_index()


# In[258]:


# pivot table for better view

month_city =pd.pivot_table(data=customer_spend,values='Amount',index='City',columns='Monthly',aggfunc='sum')


# In[259]:


month_city


# In[260]:


month_city.plot(kind="bar",figsize=(20,10),width=1)
plt.show()


# #### b. Comparison of yearly spend on air tickets 

# In[261]:


customer_spend.head()


# In[262]:


spend_type = customer_spend.groupby(["Year","Type"])[["Amount"]].sum().reset_index()


# In[263]:


spend_type


# In[264]:


air=spend_type.loc[spend_type["Type"]=="AIR TICKET"]


# In[265]:


air


# In[266]:


plt.bar(air["Year"],height=air["Amount"],color="green")
plt.xlabel("Year")
plt.ylabel("Amount Spent")
plt.title("yearly spend on air tickets")
plt.show()


# #### c. Comparison of monthly spend for each product (look for any seasonality that exists in terms of spend)

# In[267]:


customer_spend.head()


# In[268]:


# pivot table for better view

product_data = pd.pivot_table(data=customer_spend,
                              index='Product',
                              columns='Monthly',
                              values='Amount',
                              aggfunc='sum'
                             )


# In[269]:


product_data


# In[270]:


product_data.plot(kind="bar",figsize=(20,10),width=1)
plt.ylabel("Amount Spend")
plt.title("Amount spent monthly on different products")
plt.show()


# ### 5. Write user defined PYTHON function to perform the following analysis:
# 
# You need to find top 10 customers for each city in terms of their repayment amount by 
# different products and by different time periods i.e. year or month. The user should be able 
# to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the 
# function should automatically take these inputs while identifying the top 10 customers.

# In[271]:


customer_Repayment.head()


# In[272]:


customer_Repayment['Month'] = pd.to_datetime(customer_Repayment['Month'])


# In[123]:


#creating new column "Monthly" and "Yearly" using  'Month' column

customer_Repayment['Monthly'] = customer_Repayment['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
customer_Repayment['Yearly'] = customer_Repayment['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[273]:


customer_Repayment


# In[274]:


customer_Repayment['Product'].value_counts()


# In[275]:


def analysis(product,timeperiod):
    print('Give the product name and timeperiod for which you want the data')
    if product.lower()=='gold' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Gold',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='gold' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Gold',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='silver' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Silver',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='silver' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Silver',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='platinum' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Platimum',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='platinum' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        output = pivot.loc[('Platimum',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    return output


# In[127]:


analysis('PLATINUM','monthly')


# In[ ]:




