import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib import gridspec
import numpy as np
import pandas as pd
import seaborn as sns

filename = 'titanic_data.csv'
titanic_df = pd.read_csv(filename)

################################################################
## Verifying the data set for missing, not clean or non - unifom values.
count_data = titanic_df[['PassengerId','Survived','Sex','Pclass']].count()
unique_survived = np.unique(titanic_df[['Survived']].values)
unique_sex = np.unique(titanic_df[['Sex']].values)
unique_pclass = np.unique(titanic_df[['Pclass']].values)

if False:
    print count_data
    print unique_survived
    print unique_sex
    print unique_pclass


###############################################################
## Grouping data by gender (male, female) and class (1,2,3).
grouped_gen_class = titanic_df.groupby(['Sex','Pclass'])


################################################################
## Data for female pasangers:
## data_sum_f - number of female survivors
## data_count_f - number of female pasangers
## class_f - array of classes of female passengers 
## rate_f - proportion of female passanger survivors
## rate_f_total - proportion of all female passanger survivors

data_sum_f =  grouped_gen_class.sum()['Survived']['female']
data_count_f = grouped_gen_class.count()['Survived']['female']
class_f = data_sum_f.keys().values
rate_f = (data_sum_f / data_count_f) * 100

total_f = data_count_f.sum()
total_survived_f = data_sum_f.sum()
rate_total_f = int(total_survived_f / float(total_f ) * 100)


################################################################
## Data for male pasangers:
## data_sum_m - number of male survivors
## data_count_m - number of male pasangers
## class_m - array of classes of male passengers 
## rate_m - proportion of male passanger survivors

data_sum_m =  grouped_gen_class.sum()['Survived']['male']
data_count_m = grouped_gen_class.count()['Survived']['male']
class_m = data_sum_m.keys().values
rate_m = (data_sum_m / data_count_m) * 100

total_m = data_count_m.sum()
total_survived_m = data_sum_m.sum()
rate_total_m = int(total_survived_m / float(total_m) * 100)


 
##############################################################
## Creating the bar plot #1  - "Titanic" survival rate based on gender and class.
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
fig = plt.figure(figsize=(12, 6)) 

rate_genders = pd.concat([rate_f,rate_m])
levels = np.concatenate((class_f, class_m))

survival_rate = pd.Series(
    rate_genders,
    index = levels
)

gs0 = plt.subplot(gs[0])
plot_1 = survival_rate.plot(
	kind='bar',
    color='rgbcmy',
    width=0.7,  
    position=1.5,
    alpha=0.8
)

##############################################################
## Data for the bar plot #2 - "Titanic" survival rate based on gender.
rate = [rate_total_f,rate_total_m]

survival_rate_total = pd.Series(
    rate,
    index = ['female','male']
)

gs1 = plt.subplot(gs[1])
plot_2 = survival_rate_total.plot(
    kind='bar',
    color='rc',
    width=0.5,  
    position=1.5,
    alpha=0.8
)

###########################################################
## Data for the Info Labels for the bars 
## categories - values for the bar plots x axis.

## Formating label text for bar graph #1
categories = grouped_gen_class.count()['Survived'].keys()

for i,rect in enumerate(plot_1.patches):
    height = rect.get_height()
    plot_1.text(rect.get_x() + rect.get_width()/2.,\
            height-1,\
            '{},\nClass {},\n{}%'.format(categories[i][0].title(), categories[i][1], int(height)),\
            ha='center', va='top')  


## Formating label text for bar graph #2
categories_total = ['Female','Male']

for i,rect in enumerate(plot_2.patches):
    height = rect.get_height()
    plot_2.text(rect.get_x() + rect.get_width()/2.,\
            height-1,\
            '{},\n{}%'.format(categories_total[i], int(height)),\
            ha='center', va='top')  


## Ploting bar graph
plot_1.axes.get_xaxis().set_visible(False)
plt.ylabel('Survived, %')
gs0.set_title('"Titanic" survival rate based on gender and class.')


plot_2.axes.get_xaxis().set_visible(False)
plt.ylabel('Survived, %')
gs1.set_title('"Titanic" survival rate based on gender.')

plt.show()

