# Yellow JackEats

## Inspiration

As students, we have seen both the highs and the lows of on-campus dining halls. Sometimes, going to a dining hall is inconvenient given our academic and work schedule, not to mention super long lines.

We spoke with our peers about some of their dining frustrations. And so, given the ongoing rise in digital gig economy apps like Uber and Doordash, we found a glaring opportunity in an on-campus dining hall delivery service for college students.

## What it does

Yellow JackEats is a web app that provides a dynamic marketplace for dining hall food delivery. Our platform enables students to (a) make orders from any dining halls on campus and (b) sign up to deliver meals to others.

Some benefits of Yellow JackEats include...
- Convenient on-demand delivery
- Source of income for students who deliver
- Shorter dining hall lines
- A dashboard of popular orders for the dining hall staff to plan the menu accordingly


## How we built it

Our web app was written with a Python-Flask backend and a HTML/CSS/JS frontend. We also made use of Bootstrap's minimalistic and dynamic styling frameworks for the frontend.

On the backend, we built our user authentication system using SQLAlchemy where we created a database for all users and orders. Using Python's beautifulsoup library, we scraped data from Tech Dining's Nutrislice webpage which contains live menus. This allowed us to create checbox forms for each on-campus dining hall locations for students to order from. And finally, we used Twilio API to send the customer a notification when a student decides to deliver the customer's meal.

## Challenges we ran into

The two biggest challenges that we ran into were in the database for user authentication and scraping Tech Dining's menu website.

With SQLAlchemy, we found that entering in user data was quite straightforward. However, since we were relatively new with SQL, we found it very challenging to create table structures that allowed us to retrieve and update data (since we updated users' accounts every time an order was made).

Additionally, it was quite complicated to scrape the data from the Tech Dining website due to the layout of the menu. The menu was organized by day of the week, so we had to determine the day of the week and filter accordingly. We also had to make sure that students were able to order breakfast items during breakfast time, lunch items during lunchtime, etc.

## Accomplishments that we're proud of

We are proud of how we managed to make our delivery service user-friendly using a very straightforward navigational bar. We are also proud of how our website can handle new users logging in, ordering, and delivering concurrently from multiple devices. This means that our project has the potential to be scaled to a large user base.


## What we learned

Given the user authentication, ordering, and delivery capabilities, our web app had many pages. Thus, we spent a lot of time organizing many html pages which began with diagramming mockups. Approaching this web app from diagrams as opposed to immediate coding allowed us to subdivide the app into multiple screen frames. So we learned how to organize complex web file directories and consolidate this on a user-friendly website. 

Additionally, we learned a lot about SQL commands which we used to put, access, update, and remove entries from our user and order database. Having completed this project, we definitely feel a lot more confident in our abilities to work with large-scale databases going forwards.

## What's next for Yellow JackEats

We are super excited for the future of Yellow JackEats, but there are some additional steps needed before a campus launch. Firstly, we would like to deploy our web app to a hosted domain on Heroku, Netlify, etc.

Additionally, we would like to find a way to connect with BuzzCard technology so that the delivered meal can be appropriately accounted for on the orderer's meal plan. This can be achieved by giving all deliverers a RFID that models the BuzzCard every time they accept on order, or we can create a scannable QR code that enables digital meal plan verification.

Yellow JackEats,
Fulfilling Tech's appetite one delivery at a time :)
