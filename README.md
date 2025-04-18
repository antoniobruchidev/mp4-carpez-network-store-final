# E-commerce Application
Full stack e-commerce platform

## Live demo at [Carpez Network Store](https://carpez-network-store-9da961f19555.herokuapp.com/)

## Table of Contents
  - [UX](#ux)
  - [User stories](#user-stories)
    - [Strategy](#strategy)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Surface](#surface)
  - [Technologies](#technologies)
  - [Testing](#testing)
    - [Application](#applications)
    - [Allauth](#allauth)
    - [Navbar](#navbar)
  - [Deployment](#deployment)
  - [Credits](#credits)
    - [Acknowledgements](#acknowledgements)

## UX

### User Stories
- As an USER or an ADMIN, I want the platform to be intuitive.
- As an USER, I want to be able to search the products, including sorting and filtering.
- As an USER, I want to be able to purchase one or more items.
- As an USER, I want to be able to track the status of my orders.
- As an USER, I want to be notified when the status of my order changes.
- As an USER, I would like to be able to leave reviews for the products I purchased.
- As an USER, I would like to be able to read reviews from other customers. 
- As an USER, I would like to earn loyalty points to be used in discounts.
- As an ADMIN, I want to be able to add, edit and remove products. 
- As an ADMIN, I want to be able to search for a given order with the order number. 
- As an ADMIN, I want to be able to search for a given product with the relative sku. 
- As an ADMIN, I want to be able to answer reviews and send customers emails. 
- As an ADMIN, I want to be able to add and remove tags, brands, categories and discounts. 
- As an ADMIN, I want to be able to change an order status.
- As an ADMIN, I want to be able to add a product. 

### Strategy
The goal of this project is to create an intuitive e-commerce platform.

### Scope
The platform is designed to be comprehensive of an easy to use set of functions.

### Structure

The platform is a multi page web application, all build on top of the base templates. The structure features a top navigation that redirects the user to products, laptop and desktop pages, a link to email the store and a dropdown with login and register link if user is not logged in, otherwise with links for the dashboard and the shopping cart if the user is not an ADMIN while links will be for dashboard and add a product if the user is effectivly an ADMIN.
On mobile the four navigation link will collapse in four buttons stacked in vertical with the login register dropdown between the logo and menu trigger.

**Website Sections:**
| Section                | Content                                                                                                         |
|------------------------|-----------------------------------------------------------------------------------------------------------------|
| Landing page           | A nice carousel with the products having the clearance tag                                                      |
| Products page          | A list of cards of the products and ways to sort and filter them                                                |
| Product details page   | The detailed card of the product with with different actions to do if USER or ADMIN                             |
| Edit product page      | All the current details of the product ready to be changed                                                      |
| Dashboard page         | Profile page with orders, points and reviews to share if USER, a complete overview of the platform if ADMIN     |
| Shopping cart page     | Classic shopping cart with buttons to adjust quantities and the chance to use accrued points for a discount     |
| Checkout page          | Page for secure payment                                                                                         |


### Skeleton

The website is designed to be clear and simple. Every page has the same navbar and the page content is right beneath.

### Surface

I started out whit a white background but it was too plain, especially on big screens, using tailwind css yellow-50 for background and the white background cards with rounded corners makes the platform warmer and the cards stands out quite well.


## Technologies

1. python 3.12 - To create a django application.
2. django 5.1 - To create a full-stack web application and interact with a postgres db.
3. HTML - To create django templates.
4. tailwind css - To help me with the styling.
5. flowbite - To help me with the styling.
6. Font Awesome - Icons.
7. JS - For frontend flow and data handling.
8. JQuery - For frontend flow and data handling.
9. VSCode - As an IDE.
10. stripe - As an middleman for the transactions.
10. git - For version control and deployment.
11. Heroku - For web application hosting.

## Testing

### Applications
#### [Home application](home/readme.md)
#### [Product application](products/readme.md)
#### [Bag application](bag/readme.md)
#### [Checkout application](checkout/readme.md)
#### [Dashboard application](dashboard/readme.md)
#### [Reviews application](reviews/readme.md)
#### [Email relay application](email_relay/readme.md)
#### Allauth
As I had that problem described (here)[email_relay/readme.md], I also had to override a allauth registration flow or it would still throw an application error everytime an user register, or forgets the email. I created a custom adapter to override the render_mail method to prep the email to be sent and the send_mail method to post the data to the same Flask app the email_relay app interact with.
#### Navbar
The navbar comprehends four button and a dropdown. on mobile the four button collapse into a classic mobile menu.
On the dropdown there also is a popover, triggered by hovering on desktop and by click on touchscreens.
The popover is on the left on desktop at the bottom on touchscreens.
The popover is shown only when user if present is not a superuser and there is a grand total present.
The popover successfully show the cart content.
dropdown successfully shows shopping cart button only if grand total is present.

## Deployment
The deployment process on Heroku platform is quite straightforward, once created the application by clicking the "New" button in the dashboard and following instructions, go to the deploy tab, from there it's possible either to deploy using heroku-cli or to connect the app to your application git repository on github. With that option is possible either to enable automatic deploys (everytime github repository changes it deploys the new version), or manually deploy it from the repository.
If the application is developed locally in docker which is not the case it can be also be deployed by docker container registry using heroku-cli.
This app has been deployed manually.
### Heroku launch files
#### Procfile
It will tell the heroku platform how to launch the application
```bash
web: gunicorn ecommerce.wsgi:application
```
#### .python-version (Optional)
It will tell the heroku platform which version of python to use for the build. If file not present heroku platform will use its default (currently 3.13)
```bash
3.12
```
### Python environment - pip-tools required
requirements.txt compiled with
```bash
pip-compile requirements/requirements.in -o requirements.txt
```
### Environment variables
Environment variables can be set in the settings tab of the application in the heroku dashboard.

## Credits

### Acknowledgements
- My mentor, Medale Oluwafemi, for his invaluable guidance.