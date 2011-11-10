- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Title:			Project 4: Free Food!
Author : 		Christian Reyes 
Description:    README for project
Course:         05-433D SSUI Web Lab
Created : 		27 Oct 2011
Modified : 		09 Nov 2011
- - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Live app link: http://cmufreenoms.appspot.com

Information:

CMU Free Noms! tracks food reports from students about free food. Students can easily search the food reports based on the description and location.

Students need to have a Google Account in order to post reports or to find food.

The application redirects the user to the intended destination once the user has logged in. For example, the user is not logged in and attempts to visit /report . The application redirects the user to the login page to login, then redirects the user to /report as a logged in user.

Links:

Reporting a food:	http://cmufreenoms.appspot.com/report
Finding food:		http://cmufreenoms.appspot.com/find
Finding food:		http://cmufreenoms.appspot.com/find/food_name

To Report a Food:

Description must be provided. Foods should be hash-tagged. For example: free #pizza and #soda

Location must be provided. For instance, "Porter Hall 226B or GHC 6615"

Client-side javascript validation is in place to prevent the user from submitting a food report without filling out the description and location.

Finding food:

Users can find food by visually scanning the list or by using the search features. 

The user can type into the textbox titled "Search" and the page will filter the food reports without reloading the page. The url also changes so that the user can save that particular search in a bookmark for easy access later. For instance, if the user searches for "pizza", the url changes to http://cmufreenoms.appspot.com/find/pizza which allows the user easy access to that search.

The user can also slide the slider to change the time window for the search. The default is two hours from now. Clicking on the locations in the reports or the food tags will perform a search under that information without reloading the page. This allows the user to quickly search.

Backend

Google App Engine Datastore is used to store the food reports.

Django templates were used for rendering the HTML pages. I made a base template called base.html. The other templates extend the base so that the same code does not have to be repeated for every page.

Google App Engine does not store timezones when storing datetimes into the datastore. I am translating the datetimes to Eastern time in order to display properly. This is well known issue with Google App Engine. I'm using the pytc module.