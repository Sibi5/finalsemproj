import pandas as pd
import numpy as np
import xgboost as xgb 
import pickle


df = pd.read_csv('IPL_Ball_by_Ball_2008_2022.csv')
df_venue =  pd.read_csv('IPL_Matches_Result_2008_2022.csv')

df = df.replace(['Delhi Daredevils'],"Delhi Capitals")
df = df.replace(['Deccan Chargers'],"Sunrisers Hyderabad")
df = df.replace(['Rising Pune Supergiant'],'Rising Pune Supergiants')
df = df.replace(['Kings XI Punjab'],'Punjab Kings')
df = df.replace(['Gujarat Lions'],'Gujarat Titans')

df_venue = df_venue.replace(['Arun Jaitley Stadium','Feroz Shah Kotla'],"Arun Jaitley Stadium, Delhi")
df_venue = df_venue.replace(['Brabourne Stadium'],"Brabourne Stadium, Mumbai")
df_venue = df_venue.replace(['Eden Gardens'],"Eden Gardens, Kolkata")
df_venue = df_venue.replace(['Brabourne Stadium'],"Brabourne Stadium, Mumbai")
df_venue = df_venue.replace(['M Chinnaswamy Stadium',"M.Chinnaswamy Stadium"],"M Chinnaswamy Stadium")
df_venue = df_venue.replace(['MA Chidambaram Stadium, Chepauk',"MA Chidambaram Stadium, Chepauk, Chennai"],"MA Chidambaram Stadium")
df_venue = df_venue.replace(["Punjab Cricket Association IS Bindra Stadium, Mohali","Punjab Cricket Association IS Bindra Stadium","Punjab Cricket Association Stadium, Mohali"],"Punjab Cricket Association Stadium, Mohali")
df_venue = df_venue.replace(['Wankhede Stadium',"Wankhede Stadium, Mumbai","Maharashtra Cricket Association Stadium"],"Wankhede Stadium")
df_venue = df_venue.replace(['Rajiv Gandhi International Stadium, Uppal',"Rajiv Gandhi International Stadium"],"Rajiv Gandhi International Stadium")
df_venue = df_venue.replace(['Sardar Patel Stadium, Motera'],'Narendra Modi Stadium, Ahmedabad')

df_venue =df_venue.replace(['Delhi Daredevils'],"Delhi Capitals")
df_venue= df_venue.replace(['Deccan Chargers'],"Sunrisers Hyderabad")
df_venue= df_venue.replace(['Rising Pune Supergiant'],'Rising Pune Supergiants')
df_venue = df_venue.replace(['Kings XI Punjab'],'Punjab Kings')
df_venue = df_venue.replace(['Gujarat Lions'],'Gujarat Titans')

team_ids = {}
for i,v in enumerate (list(df['BattingTeam'].unique())):
  team_ids[v] = int(i)
print(team_ids)

venue_ids = {}
for i,v in enumerate (list(df_venue['Venue'].unique())):
  venue_ids[v] = int(i)
print(venue_ids)

venue_ids["Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium"] = 36

#df= df[(df['overs'] < 6.0)]
df=df[(df['ID']>=1136561)]
df_venue=df_venue[(df_venue['ID']>=1136561)]

finaldata = pd.DataFrame(columns=['match_id','BattingTeam','ppruns','venue'])

match_id =list(df['ID'].unique())
for match in match_id:
    if not (((df_venue[(df_venue['ID'] == match)]['WinningTeam'])).isnull().any()):
        runs = df[(df['ID'] == match) & (df['innings'] == 1)]['total_run'].sum() 
        batting_team_name = list((df[(df['ID'] == match) & (df['innings'] == 1)]['BattingTeam']).unique())
        venue = list((df_venue[(df_venue['ID'] == match)]['Venue']))[0]
        venue = venue_ids[venue]
        team1 = list((df_venue[(df_venue['ID'] == match)]['Team1']))
        team2 = list((df_venue[(df_venue['ID'] == match)]['Team2']))
        bowling_team_name = ''
        if batting_team_name == team1:
            bowling_team_name = team2
        else:
            bowling_team_name = team1
        batting_team_name = team_ids[batting_team_name[0]]
        bowling_team_name = team_ids[bowling_team_name[0]]
        inn=1
        new_data = pd.DataFrame({'match_id': [match],'innings': [inn],'BattingTeam': [batting_team_name], 'BowlingTeam': [bowling_team_name], 'ppruns': [runs],'venue': [venue]})
        finaldata = pd.concat([finaldata, new_data], ignore_index=True)

match_id =list(df['ID'].unique())
for match in match_id:
    if not (((df_venue[(df_venue['ID'] == match)]['WinningTeam'])).isnull().any()):
        runs = df[(df['ID'] == match) & (df['innings'] == 2)]['total_run'].sum() 
        batting_team_name = list((df[(df['ID'] == match) & (df['innings'] == 1)]['BattingTeam']).unique())
        venue = list((df_venue[(df_venue['ID'] == match)]['Venue']))[0]
        venue = venue_ids[venue]
        team1 = list((df_venue[(df_venue['ID'] == match)]['Team1']))
        team2 = list((df_venue[(df_venue['ID'] == match)]['Team2']))
        bowling_team_name = ''
        if batting_team_name == team1:
            bowling_team_name = team2
        else:
            bowling_team_name = team1
        batting_team_name = team_ids[batting_team_name[0]]
        bowling_team_name = team_ids[bowling_team_name[0]]
        inn=2
        new_data = pd.DataFrame({'match_id': [match],'innings': [inn],'BattingTeam': [batting_team_name], 'BowlingTeam': [bowling_team_name], 'ppruns': [runs],'venue': [venue]})
        finaldata = pd.concat([finaldata, new_data], ignore_index=True)

finaldata = finaldata.sort_values(by=['match_id','innings'], ascending=[False,True])

x = finaldata.drop(['ppruns','match_id'], axis=1)
y = finaldata['ppruns']

convert_dict = {'BattingTeam': int,
                'innings': int,
                'venue' : int
                }
x = x.astype(convert_dict)

model = xgb.XGBRegressor()
model.fit(x, y)

y_pred = model.predict(x)

'''for i in range(len(y)):
  print(y[i],y_pred[i])'''

#venue1 = input("Enter venue : ")
venue1 = "Narendra Modi Stadium, Ahmedabad"
print("Enter innings 1: ")
innings1 = 1
#batting_team1 = input("Enter batting team 1: ")
batting_team1 = "Gujarat Titans"
#bowling_team1 = input("Enter bowling team 1: ")
bowling_team1="Chennai Super Kings"
#print("Enter innings 1: ")
innings2 = 2
batting_team2 = bowling_team1
bowling_team2 = batting_team1
venue2 = venue1

data = [
    {
        'innings': innings1,
        'batting_team': batting_team1,
        'bowling_team': bowling_team1,
        'venue': venue1
    },
    {
        'innings': innings2,
        'batting_team': batting_team2,
        'bowling_team': bowling_team2,
        'venue': venue2
    }
]

df_test = pd.DataFrame(data)

print(df_test)

test_data_final = pd.DataFrame()
test_data_list = []
test_data_list.append({'BattingTeam':team_ids[df_test.iloc[0]['batting_team']], 'venue':venue_ids[df_test.iloc[0]['venue']],'innings':df_test.iloc[0]['innings'], 'BowlingTeam':team_ids[df_test.iloc[0]['bowling_team']], })
test_data_list.append({'BattingTeam':team_ids[df_test.iloc[1]['batting_team']],'venue':venue_ids[df_test.iloc[0]['venue']], 'innings':df_test.iloc[1]['innings'], 'BowlingTeam':team_ids[df_test.iloc[1]['bowling_team']], })
test_data_final = pd.DataFrame(test_data_list)
test_data_final['unique_index'] = range(len(test_data_final)) 
test_data_final.set_index('unique_index', inplace=True)  

x_test = test_data_final
y_test_pred = model.predict(x_test)

print("Powerplay score is : ",y_test_pred)

team1=y_test_pred[0]
team2=y_test_pred[1]

'''if team1 > team2 :
  winner=df_test.batting_team[0]
else:
  winner=df_test.bowling_team[0]

print(winner)'''


pickle_out = open("score0.pkl", "wb")
pickle.dump(model, pickle_out)
pickle_out.close()









