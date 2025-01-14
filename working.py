# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:44:35 2025

@author: tayta

This is a set of code that is made while following an API tutorial on youtube.

API is Application Programming Interface. It is a program that sends out a request and will grab information. 
An example of this given by the youtube video maker is an Amazon Inventory system. It isn't installed onto your computer, but instead on a server where the website is your connection.
When looking up an item, the website sets a request to get information about that item, the API sends it back and then is displayed on the page. It follows suit that when you click on an 
    item that you want to see, it'll send a request to get information on the one item, then sends it back and displays. (this might not be true, but a good idea of what is going on)

FASTAPI is a fast way to implement/make API's. It has several advantages:
    1. Data Validation: prevents variables/instances from having different data types.
    2. Auto Documentation: automatically mades documentation (webpages) to see what is expected for the api program. 
    3. Auto Completion and Code Suggestions: faster running and gives tips. 
    
    
Steps from the tutorial:
    1. Install fastapi and unicorn on the system, in this case I used the command "pip install fastapi/uvicorn".
    2. Import fastapi in script and test to make sure it is found by running.
    3. Import FastAPI from fastapi.
    4. Create an object of FastAPI(), in this cass app
    5. Create an endpoint, this is the url or location that is going to be connected to. This would be represented by a url with an / and location.
        In this case, we use "/" to represent local device.
    6. Create a function/method with a decorator "@app.get(endpoint)".
    7. In cammand promp for windows, change directory to the python program and type "python -m uvicorn name_of_program_without_.py:name_of_FastAPI_variable --reload".
        This will run the code and return a bunch of information as well as an address to be able to access the api doc (where the http:// is found). 
    8. If putting the address into a web browser, itll come up with what ever is being returned from the function. If you type the address plus '/docs' it will bring up the documentation
        of the API/function.
    9. Create more endpoints by doing the decorator with the inside being the name of the tab.
    10. Creating path parameters is done by typing in the address bar the input. Ie, looking at the inventory dictionary and the get_item function, when typing in the address and then "/get-item/1" 
        we are returned the information in the dictionary based on that number.
    11. Multiple path parameters is as easy as just adding another '/{object}' in the decorator and the function parameter list. 
    12. Importing Path from the fastapi library, we can set more constraints onto our path parameters. In this case, I made a function similar to the get_item called item_get that uses Path as a parameter. 
        Now when the code is ran and seen on the /docs, the item_get has a description that is what is put down in the path paramter.
    13. Path can also include limits/constraints on values by putting 'gt: greater than, lt: less than, le: less than or equal to, ge: greater than or equal to'. This prevents any numbers outside of the constraints to throw an error.
        Now, when the address bar has 'address/item-get/0' or '/2' it will throw an error. But when it has a 1, itll work as intended. 
    14. Now, its introducting QUERRY PARAMETERS. This is when a url has a ? and then some values or whater after it. In this case, the function get_name is made to find the item info based on the name of the item.
        So, when searching for it, the address will have "address/get-by-name?name=Milk" to get the dictionary item that contains milk in it. When searching for other items or dict keys, can change the 'name' to 'price' or 'brand'
    15. If we want the querry parameter to be an option, we can set a default value. ie, name: str = None. When we have an optional querry parameter, the FASTAPi suggests from typing import Optional and using that instead. ie, 'name: Optional[str] = None'.
        Python gets angry whenever a Mandatory parameter is put after a non-Mandatory parameter, so put optional parameters after the necessary ones. 
    16. Now we can combine path parameters and querry parameters. This is done by changing the decorator to have the path parameter as an input like the item-get or get-item, and then having the querry parameters in the parameter list as well. 
        In this case, I made a function called get-from-name (in the decorator) that takes in an item_id and a test to determine what is done (not very well but just as the example)
        
    17. Not starting into POST, make a function with decorator app.post('/name_of_whater') that will do something. In this case, we make a decorator/function that will create an item in the dictionary, so its @app.post('/create-item').
        This however needs a class that will makes items for us using this function, so: 'from pydantic import BaseModel'.
        
        When doing the inventory[item_id] = item in this function, we are making it so that the dictionary is holding the class object and not the info specifically, so the .get() will need to be changed to better suit finding a class objects variables.
        
        For the example, the filled inventory dict has been commented out and a new empty one was made to try the create-item. Now, when loaded into the /docs and looking at the create item, you can try it out and put in values for the item_id and then 
            put in values for the different variables.
            
    18. Now for the PUT, which updates information. For this case, we make a class called UpdateItem that makes the variables optional so that it doesn't need to use all of the variable to update. This is then tested using the querry parameters or you can 
        test it using the body in the /docs
        
    19. The next method is the DELETE method which removed information. In this case, we will be removing an Item from the inventory list, relatevily straight forwardly. 
    
    20. Lastly, there are status codes that can be returned whenever there is something that happened, ie, 200: good, 201: error, 404:not found. In some of the functions below, there is "return {}", but we can make it raise an exception. this is shown in
        the get-from-name where it will raise an execption using the status code 404 not found, or the update_item function when an item isn't found, it raises the status code and details given to it.'
        
"""

from fastapi import FastAPI
from fastapi import Path
from fastapi import Query
from fastapi import HTTPException, status

from typing import Optional
from pydantic import BaseModel


app = FastAPI() #required start


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    
    
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# The different core http methods:
    # GET. Grabbing data from url
    # POST. Putting information into the url
    # PUT. Update something that is already existing
    # DELETE. Deleting information


#The root 
@app.get('/') #home
def home(): #function called for a specific operation
    return {'Data': 'Testing'} #FastAPI actually ends up converting this Dictionary into a JSON (JavaScriptObject) when returning. Just know, anything returned may end up different when recieved. 

@app.get('/about')
def about():
    return {'Data':'About'}

# inventory = {
#                 1: {'name': 'Milk',
#                     'price':3.99,
#                     'brand':'regular'}
                
#             }

inventory = {}

@app.get('/get-inventory')
def get_inventory():
    return inventory

@app.get('/get-item/{item_id}/{name}') #the {} asks for an input, then is put into the function. 
def get_item(item_id: int, name: str):
    return inventory[item_id]

@app.get('/item-get/{item_id}')
def item_get(item_id: int = Path(description='The ID of the item you would like to view', 
                                 gt = 0,)): #path(description= 'message to be shown to user when looking over the documentation', gt = #, lt = #)
    return inventory[item_id]

@app.get('/get-by-name')
def get_name(test: int, name: Optional[str] = None):
    if test == 1:
        for item_id in inventory:
            if inventory[item_id]['name'] == name:
                return inventory[item_id]
    
    return {'Data':'Not Found'}

@app.get('/get-from-name/{item_id}')
def name_get(test: int, item_id: int, name: Optional[str] = None):
    if test == 1: #going by name
        for item_id in inventory:
            if inventory[item_id].name == name:
                return inventory[item_id]
    if test == 2:
        return inventory[item_id]
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)




@app.post('/create-item/{item_id}') 
def create_item(item_id: int, item: UpdateItem): #the decorator and the Item tells the program that we are sending information, not trying to get information back. 
    if item_id in inventory:
        return {'Error': 'Item ID already exists'}
    inventory[item_id] = item
    return inventory[item_id]

@app.put('/update-item/{item_id}')
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code= 404, detail= 'Item Not Found')
    
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete('/delete-item')
def delete_item(item_id: int = Query(...,description= 'The ID of the item to delete', gt = 0)):
    if item_id not in inventory:
        return {'Error':"ID does not exist"}
    del inventory[item_id]
    return {'Data':"Item Deleted"}