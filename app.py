from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample cutoff data
cutoff_data = [
     {
      "college": "Bangalore Medical College",
      "closing_rank": 13570,
      "state": "Karnataka",
      "category": "GEN"
    },
    {
      "college": "Dr. B. R. Ambedkar Medical College",
      "closing_rank": 60701,
      "state": "Karnataka",
      "category": "GEN"
    },
    {
      "college": "Kempegowda Institute of Medical Sciences",
      "closing_rank": 47447,
      "state": "Karnataka",
      "category": "OBC"
    },
    {
      "college": "M. S. Ramaiah Medical College",
      "closing_rank": 47177,
      "state": "Karnataka",
      "category": "SC"
    },
    {
      "college": "Khaja Bande Navaz Institute of Medical Sciences",
      "closing_rank": 88343,
      "state": "Karnataka",
      "category": "ST"
    }
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug: print incoming data

        rank = data['rank']  # Get the rank from the request
        category = data['category']
        state = data['state']

        # Filter the colleges based on score, category, and state
        filtered_colleges = [
            college for college in cutoff_data
            if college['state'] == state and college['category'] == category and college['closing_rank'] >= rank
        ]
        
        print(f"Filtered Colleges: {filtered_colleges}")  # Debug: print the filtered colleges

        # If there are no colleges that match, try to offer alternative options
        if not filtered_colleges:
            alternative_colleges = [
                college for college in cutoff_data
                if college['state'] == state and college['category'] == category and college['closing_rank'] > rank
            ]
            print(f"Alternative Colleges: {alternative_colleges}")  # Debug: print alternative colleges

            # Respond with alternative colleges
            return jsonify({"message": "No colleges found matching your exact criteria.", "alternative_colleges": alternative_colleges})

        # If matching colleges are found, respond with them
        return jsonify({"allocated_colleges": filtered_colleges})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500

if __name__ == "__main__":
    app.run(debug=True)
