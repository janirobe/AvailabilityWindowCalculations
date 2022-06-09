import pandas as pd

dfActivity = pd.read_csv("../AvailabilityWindowPrepList/activities.csv")
dfContacts = pd.read_csv("../AvailabilityWindowPrepList/contacts.csv")

#filter only columns we need
dfActivity = dfActivity.filter(items=['Activity Type','Activity Date','Target Contact :: AlexID'])
dfActivity = dfActivity.rename(columns = {'Target Contact :: AlexID':'AlexID'})

#filter out non first intake activities
dfActivity = dfActivity[dfActivity['Activity Type'].str.match('First Intake -')]

#create new column by separating by space delimiter
dfActivity['New Activity Date'] = dfActivity['Activity Date'].str.split(' ').str[0] 

#converting activity columns to date time
dfActivity['New Activity Date'] = pd.to_datetime(dfActivity['New Activity Date'])
#sort by date (descending)
dfActivity = dfActivity.sort_values(by='New Activity Date', ascending=True)

#filter out old date column
dfActivity = dfActivity.filter(items=['Activity Type','New Activity Date','AlexID'])
dfActivity = dfActivity.rename(columns = {'New Activity Date':'Activity Date'})

#dropping duplicates (AlexId and First Intake Type), keeping the earliest ones (oldest)
dfActivity = dfActivity.drop_duplicates(['Activity Type','AlexID'],keep= 'first')

#filter out all rows that have null AlexID
dfActivity = dfActivity[dfActivity['AlexID'].notnull()]

#pivot activites for all first intake dates are horizontal
dfActivity = dfActivity.pivot_table('Activity Date', ['AlexID'], 'Activity Type')

##filter out all values that don't have AlexID
dfContacts = dfContacts[dfContacts['AlexID'].notnull()]



##MERGE
#df = pd.merge(dfContacts, dfActivity, on=['AlexID'])
df = dfContacts.merge(dfActivity, how='left', on =['AlexID'])

#removing spaces of columns and using a (.) separator
df.columns = df.columns.str.replace('-', '.')

## Adding a (.) and an index number to all first intake column name
index = 1
for col in df[df.columns[pd.Series(df.columns).str.startswith('First Intake .')]].columns:
    newVal = col
    newVal += "."
    newVal += str(index)
    index += 1
    df = df.rename(columns={col:newVal})


df = df.drop([0])
df.to_csv('1.OUTPUT_intakeDates.csv')