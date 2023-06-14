from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from pymongo import MongoClient
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)
model = joblib.load('score0.pkl')
powerplay_model = joblib.load('powerplay0.pkl')  
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  
collection = db['matches']  

@app.route('/api/matches', methods=['POST'])
def create_match():
    data = request.json
    venue = data['venue']
    team1 = data['team1']
    team2 = data['team2']
    innings1 = 1
    innings2 = 2
    bowling_team1 = team2
    bowling_team2 = team1
    venue2 = venue

    team_ids = {'Rajasthan Royals': 0, 'Gujarat Titans': 1, 'Royal Challengers Bangalore': 2, 'Lucknow Super Giants': 3, 'Sunrisers Hyderabad': 4, 'Punjab Kings': 5, 'Delhi Capitals': 6, 'Mumbai Indians': 7, 'Chennai Super Kings': 8, 'Kolkata Knight Riders': 9, 'Rising Pune Supergiants': 10, 'Pune Warriors': 11, 'Kochi Tuskers Kerala': 12}
    
    venue_ids = {'Narendra Modi Stadium, Ahmedabad': 0, 'Eden Gardens, Kolkata': 1, 'Wankhede Stadium': 2, 'Brabourne Stadium, Mumbai': 3, 'Dr DY Patil Sports Academy, Mumbai': 4, 'Maharashtra Cricket Association Stadium, Pune': 5, 'Dubai International Cricket Stadium': 6, 'Sharjah Cricket Stadium': 7, 'Zayed Cricket Stadium, Abu Dhabi': 8, 'Arun Jaitley Stadium, Delhi': 9, 'MA Chidambaram Stadium': 10, 'Sheikh Zayed Stadium': 11, 'Rajiv Gandhi International Stadium': 12, 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium': 13, 'Punjab Cricket Association Stadium, Mohali': 14, 'M Chinnaswamy Stadium': 15, 'Sawai Mansingh Stadium': 16, 'Holkar Cricket Stadium': 17, 'Green Park': 18, 'Saurashtra Cricket Association Stadium': 19, 'Shaheed Veer Narayan Singh International Stadium': 20, 'JSCA International Stadium Complex': 21, 'Barabati Stadium': 22, 'Subrata Roy Sahara Stadium': 23, 'Himachal Pradesh Cricket Association Stadium': 24, 'Dr DY Patil Sports Academy': 25, 'Nehru Stadium': 26, 'Vidarbha Cricket Association Stadium, Jamtha': 27, 'New Wanderers Stadium': 28, 'SuperSport Park': 29, 'Kingsmead': 30, 'OUTsurance Oval': 31, "St George's Park": 32, 'De Beers Diamond Oval': 33, 'Buffalo Park': 34, 'Newlands': 35}
    df_test = pd.DataFrame({
        'innings': [innings1, innings2],
        'batting_team': [team1, team2],
        'bowling_team': [bowling_team1, bowling_team2],
        'venue': [venue, venue2]
    })

    test_data_final = pd.DataFrame()
    test_data_list = []
    test_data_list.append({
        'BattingTeam': team_ids[df_test.iloc[0]['batting_team']],
        'venue': venue_ids[df_test.iloc[0]['venue']],
        'innings': df_test.iloc[0]['innings'],
        'BowlingTeam': team_ids[df_test.iloc[0]['bowling_team']]
    })
    test_data_list.append({
        'BattingTeam': team_ids[df_test.iloc[1]['batting_team']],
        'venue': venue_ids[df_test.iloc[0]['venue']],
        'innings': df_test.iloc[1]['innings'],
        'BowlingTeam': team_ids[df_test.iloc[1]['bowling_team']]
    })
    test_data_final = pd.DataFrame(test_data_list)
    test_data_final['unique_index'] = range(len(test_data_final))
    test_data_final.set_index('unique_index', inplace=True)

    prediction = model.predict(test_data_final)
    prediction_bias = prediction + 15


    # Store data in MongoDB
    match = {'venue': venue, 'team1': team1, 'team2': team2,'prediction': prediction_bias.tolist()}
    result = collection.insert_one(match)

    return jsonify({'prediction': prediction_bias.tolist()})

@app.route('/api/powerplay', methods=['POST'])
def powerplay():
    data = request.json
    venue = data['venue']
    team1 = data['team1']
    team2 = data['team2']
    innings1 = 1
    innings2 = 2
    bowling_team1 = team2
    bowling_team2 = team1
    venue2 = venue

    team_ids = {'Rajasthan Royals': 0, 'Gujarat Titans': 1, 'Royal Challengers Bangalore': 2,
                'Lucknow Super Giants': 3, 'Sunrisers Hyderabad': 4, 'Punjab Kings': 5, 'Delhi Capitals': 6,
                'Mumbai Indians': 7, 'Chennai Super Kings': 8, 'Kolkata Knight Riders': 9,
                'Rising Pune Supergiants': 10, 'Pune Warriors': 11, 'Kochi Tuskers Kerala': 12}

    venue_ids = {'Narendra Modi Stadium, Ahmedabad': 0, 'Eden Gardens, Kolkata': 1, 'Wankhede Stadium': 2,
                 'Brabourne Stadium, Mumbai': 3, 'Dr DY Patil Sports Academy, Mumbai': 4,
                 'Maharashtra Cricket Association Stadium, Pune': 5, 'Dubai International Cricket Stadium': 6,
                 'Sharjah Cricket Stadium': 7, 'Zayed Cricket Stadium, Abu Dhabi': 8, 'Arun Jaitley Stadium, Delhi': 9,
                 'MA Chidambaram Stadium': 10, 'Sheikh Zayed Stadium': 11, 'Rajiv Gandhi International Stadium': 12,
                 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium': 13,
                 'Punjab Cricket Association Stadium, Mohali': 14, 'M Chinnaswamy Stadium': 15,
                 'Sawai Mansingh Stadium': 16, 'Holkar Cricket Stadium': 17, 'Green Park': 18,
                 'Saurashtra Cricket Association Stadium': 19, 'Shaheed Veer Narayan Singh International Stadium': 20,
                 'JSCA International Stadium Complex': 21, 'Barabati Stadium': 22, 'Subrata Roy Sahara Stadium': 23,
                 'Himachal Pradesh Cricket Association Stadium': 24, 'Dr DY Patil Sports Academy': 25,
                 'Nehru Stadium': 26, 'Vidarbha Cricket Association Stadium, Jamtha': 27,
                 'New Wanderers Stadium': 28, 'SuperSport Park': 29, 'Kingsmead': 30, 'OUTsurance Oval': 31,
                 "St George's Park": 32, 'De Beers Diamond Oval': 33, 'Buffalo Park': 34, 'Newlands': 35}

    df_test = pd.DataFrame({
        'innings': [innings1, innings2],
        'batting_team': [team1, team2],
        'bowling_team': [bowling_team1, bowling_team2],
        'venue': [venue, venue2]
    })

    test_data_final = pd.DataFrame()
    test_data_list = []
    test_data_list.append({
        'BattingTeam': team_ids[df_test.iloc[0]['batting_team']],
        'venue': venue_ids[df_test.iloc[0]['venue']],
        'innings': df_test.iloc[0]['innings'],
        'BowlingTeam': team_ids[df_test.iloc[0]['bowling_team']]
    })
    test_data_list.append({
        'BattingTeam': team_ids[df_test.iloc[1]['batting_team']],
        'venue': venue_ids[df_test.iloc[0]['venue']],
        'innings': df_test.iloc[1]['innings'],
        'BowlingTeam': team_ids[df_test.iloc[1]['bowling_team']]
    })
    test_data_final = pd.DataFrame(test_data_list)
    test_data_final['unique_index'] = range(len(test_data_final))
    test_data_final.set_index('unique_index', inplace=True)

    prediction_pp = powerplay_model.predict(test_data_final)  # Use powerplay model for prediction

    # Store data in MongoDB
    match = {'venue': venue, 'team1': team1, 'team2': team2, 'prediction': prediction_pp.tolist()}
    result = collection.insert_one(match)

    return jsonify({'prediction': prediction_pp.tolist()})



if __name__ == '__main__':
    app.run(debug=True)
    
