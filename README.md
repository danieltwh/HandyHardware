# BT2102Project

<!-- ABOUT THE PROJECT -->
## About The Project

![Handy Hardware](https://github.com/Onelayer/BT2102Project/blob/main/Assets/HandyHardwarev1.png)

Video link: https://drive.google.com/file/d/17yERTBopsTmJ_y-TDPSkS1S69BtWLxa0/view?usp=sharing

This is an ecommerce application with 2 distinct components. The customer page has various functions such as the ability to purchase items, view purchase history and submit service requests. The administrator page is able to track current stocks, view and approve service requests.

We used Python Tkinter for our graphical user interface, MySQL for our back-end, entity relationship modelling concepts for database design, and Git for version control.


### Built With

* Tkinter


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

<!-- ### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  
sh
  npm install npm@latest -g
  
 -->

### Installation

1. Clone the repo
   
sh
   git clone https://github.com/eryuanren/BT2102Project.git
   

### Start the application
python app.py


<!-- USAGE EXAMPLES -->
## Usage

### User Registration
This application is able to create new users and administrators, storing user information and checking for duplicates and incorrect formatting

### Product Management
Items in stock can be purchased by the user, and the stock will be updated accordingly. The purchase date will be recorded and the item warranty will be calculated from the date of purchase.

### Product Search
User can conduct a search using various parameters of the item, which shows a list of unsold items that matches the parameters. Administrators can conduct a specific search on an item using its itemID.

### Request Management
Users can submit a request for a purchased item. Items that are under warranty will not require payment, while items with an expired warranty will have to pay a service fee. A request status will be updated accordingly

### Service management
Administrators can approve requests once payment has been made (or no payment is needed), and the service status will be updated accordingly
