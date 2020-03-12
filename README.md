# SuperPool #

## Team Members: ##

Aman Kansal (170050027)
Ansh Khurana (170050035)
Arnab Jana (170100082)
Pranay Reddy Samala (170070022)

## Category: Web App ##
### Overview ###
Modern technology has transformed the marketplace worldwide. Apps and websites like Uber, Zomato, Amazon and Flipkart have redefined the relationship between consumers and producers. With just the tap of a button, customers can bring day to day services to their doorstep, giving an all new meaning to consumerism.
However, in this dynamic marketplace, there are no apps/websites which offer consumer-consumer interaction. What if you want to order food with friends? How do you find like-minded friends to go with for a movie? 
Technology at hand ignores the social aspect of the marketplace. We seek to address this void by creating “Supershare”, a user-driven platform that brings consumers together. Now no more time wasted searching for the “10th” member to avail your group discount!
Before SuperShare (real life): Call a bunch of people to find out whether they are interested. 25% will say they already watched the movie, 25% will say outright that they are not interested, and the rest will spend at least 2 hours coordinating. ( college problems :) ). 
After SuperShare (utopia): I open “SuperShare”, select the groups of people I would wish to go with, and wait to get matched. No more coordination!
Applications and Use Cases 
Food ordering - While apps like Zomato and Swiggy have completely revolutionized the way we order food, managing how the food is shared among individuals is another important aspect to consider. As of now, ordering food with friends is a major problem, since one needs to personally contact all of his/her friends to see if they are interested in ordering food on OP’s preferred day and time. Further, conflicts among which restaurant to choose makes the process more cumbersome. Further, if none of your friends are foodies/you being an introvert don’t prefer to ping people asking for sharing food then ordering food is a painful experience. We propose that none of this polling other friends and coordination is required. To simplify and revolutionize food ordering we introduce automatic matching of people ordering food on our platform. People can be matched on time of order,  cuisine, restaurant etc. From there on, we automate managing everything for our users. Maintaining dishes to order and how many people will be sharing what dishes will be easy to track and manage. We also aim to manage bills and payments within our app to create a seamless experience. 
Cab booking - Sharing cabs is beneficial for the environment as well as helps save money for frequent travellers. Sharing cabs among hostel student would be beneficial and can help in saving time and money for students. Just post the time and date of your journey in our app and we will automatically match interested people to share the journey.
Events, concerts and more - No friends? No worries. We got you covered. xD Looking for people who are interested in the same movie, concert, or any other group activity? Just mention your interest and availability and we will match you with like-minded and interested people for the same event.
Coupons and offers matching - Many times, coupons and offers released by various companies and apps are targeted at bulk/shared orders. For example, companies come up with buy 2 get 2 offers and y% off for orders above rupees x. This inhibits individual buyers from taking advantage of these offers.  To eliminate this, SuperShare will match people looking to apply the same coupon and offers. Further, we will recommend users to take advantage of these offers which are active on the basis of their recent purchase history.
E-commerce: Many e-commerce sellers apply minimum order limits. This limits many buyers who are looking for small items quickly. We plan to merge such small orders across different people to fulfil the required limits without any hassles.


### Features ###
We currently are considering implementing the following features -
For each ‘service’ that app can be used for, the user would be able to have a group of ‘friends’ with whom he’d be able to pool that particular service. 
A user can also create ‘links’ such that all people who get that link would be able to share the service with each other. This is similar to the creation of groups in WhatsApp.
People wanting to make use of a service will be able to post this. Depending upon the time they entered, the usual slackness they tolerate, and the people with whom they accept to pool the service, the app will suggest matches between people, recommending them to pool the service
Sometimes one might forget to post. For handling this the stats of users with the frequency with which they have made use of a service will be maintained (visible only to the sharers), using which one might want to ping someone if he/she would like to join.
Recommendations for becoming shareholder for particular types of items being share-initiated by somebody else, based on his/her share-history. 
There will be support for group chat corresponding to every service and there might be support for screen sharing between users as well.
While we would try to implement all the features mentioned above, the final set of features implemented would depend on feasibility and time availability.





### Details of schema, views and interfaces ###

#### Relational Schema:- ####


			Sketch plan for SuperShare_Relations_Schema

#### Terminology:- ####
Service_type - Broad categories of services (like food, shopping, travel etc).
Service - Particular service under any of the Service_type (like ‘Pizza from ABC on date XYZ’ under ‘food’).
Message - Message associated with chat in a particular service for its members.
Group - Group of users (potentially related, like WhatsApp group for HostelX, not associated with any service). Created by link sharing through external media (like whatsapp).
Current_service - All services with start-time<=current-time<=start-time+slackness
Past_service - All services with current-time>start-time+slackness

#### Materialized Views required:- ####
User_profile - Personal details
List of groups - Display all groups, which a user is a member of, and a public group for all app users.
Group - Displays all the members in that group. Here, a user can query for a service to check availability of pooling service by members of the group or start a new service.
List_of_services - List of all services an user is part of.
Service - Display metadata (details of service, members sharing the service etc.) and a chat_history (all messages within chat of that particular service sorted on timestamp).
Recommendations - Display all Current_services with the same service_type as Past_services used by that user sorted on start-time.
Design Choice:-
Joining a group is through links shared externally. When a person searches for some service in a group, our app will display all relevant matching services containing members of that group and give the user the option to join any of those groups. On joining, the user can participate in the chat of that particular service. Otherwise, the user can create a new service of a particular service-type in our app, waiting for others to join the service. There is also a public group with all users of our app, where users can be matched with potentially with any other user (if the user has no discretion).
Interfaces required:-
Authentication - For logging into our app.
Create_a_group - User can create a new group
Joining_a_group - Users can join a group using link shared on external media.
Start_Service - Initiating a new service for pooling under a particular group and service_type.
Join_existing Services - Users with “almost matching” service requirements from a group (will be displayed by our app) can join the service and hence participate in discussions within it’s chat.
Adding message to chat - Users in a service can add a message to the chat of that service.

