from park_place_info import ParkPlaceDetails
from user_location_data import UserLocationData
from parksearch import ParkSearch
import os
from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)

API_KEY = os.environ['API_KEY']


# # # TO DO # # #
# decide if modules should nest in parksearch of something different (i dont like having to reinsert
#   the users address into each park place details object!!!!)
# maybe create a meta-modules with everything inside of "test parksearch stuff"

class SortedList:

    def get_sorted_list(self, park_details_object_list):

        def sort_by_miles_away(park):
            return park.travel_details.distance

        return sorted(park_details_object_list, key=sort_by_miles_away)

    def __init__(self):

        self.list = None

# ----TEST PARKSEARCH STUFF---- #
# user_a_address = "5925 langford bay road, chestertown MD 21620"
# user_a_location_data = UserLocationData(user_a_address) # get info from user, only conduct location data once and store
# # # on server
# user_a_parksearch = ParkSearch(user_a_location_data) # rerun when looking for park
# dog_parks_place_id_list = user_a_parksearch.populate_park_id_list()
# park_details_object_list = [ParkPlaceDetails(park_id, user_a_location_data.formatted_address) for park_id in dog_parks_place_id_list]
# # allow users to signup/favorite/register different park details objects. Need to feed in seperate class object
# # when displaying park details that stores which users have favorited it
# # different states - have visited/ plan to visit again/ regularly visit/ favorite

# ----TEST GETTING ADDRESS---- #
sorted_list = SortedList()




@app.route("/", methods=("GET", "POST"))
def home_page():
    if request.method == 'POST':

        address_line_1 = request.form['address-line-1']
        address_line_2 = request.form['address-line-2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        user_reported_address = f"{address_line_1}, {address_line_2}, {city}, {state}, {zip}"
        user_location_data = UserLocationData(user_reported_address)
        user_a_parksearch = ParkSearch(user_location_data)
        dog_parks_place_id_list = user_a_parksearch.populate_park_id_list()
        park_details_object_list = [ParkPlaceDetails(park_id, user_location_data.formatted_address) for park_id in
                                    dog_parks_place_id_list]
        sorted_list.list = sorted_list.get_sorted_list(park_details_object_list)

        return redirect(url_for('search_results'))
    return render_template("user-info.html")


@app.route("/search_results")
def search_results():
    return render_template("index.html", park_details=sorted_list.list)



if __name__ == "__main__":
    app.run(debug=True)
