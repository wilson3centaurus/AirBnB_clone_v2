# AirBnB Clone v3 - RESTful API

This project is an implementation of a RESTful API for an AirBnB clone, built using Python and Flask. It aims to provide endpoints for managing various resources related to property rental.

## Authors
- Paschal Ugwu
- Amarachi Nnanta

## Overview
This project focuses on building a RESTful API for an AirBnB clone, allowing users to perform various operations such as retrieving, creating, updating, and deleting resources like states, cities, places, amenities, users, and reviews.

## Learning Objectives
By working on this project, you will gain understanding of:
- REST principles
- API concepts
- Cross-Origin Resource Sharing (CORS)
- HTTP methods for CRUD operations
- Flask web framework

## Resources
To understand the concepts and technologies used in this project, consider referring to the following resources:
- [REST API concept page](#)
- [Learn REST: A RESTful Tutorial](#)
- [Designing a RESTful API with Python and Flask](#)
- [HTTP access control (CORS)](#)
- [Flask cheatsheet](#)
- [What are Flask Blueprints, exactly?](#)
- [Flask](#)
- [Modular Applications with Blueprints](#)
- [Flask tests](#)
- [Flask-CORS](#)

## Requirements
### Python Scripts
- Allowed editors: vi, vim, emacs
- All files should end with a new line
- The first line of all files should be `#!/usr/bin/python3`
- Follow PEP 8 style guidelines (version 1.7)
- All files must be executable
- Document modules, classes, and functions appropriately
- Mandatory presence of README.md file
- Install Flask using `$ pip3 install Flask`

### Python Unit Tests
- All files should end with a new line
- Place test files inside a folder named `tests`
- Use `unittest` module
- Test files must be Python files (extension: .py)
- Test files and folders should start with `test_`
- Execute tests using `python3 -m unittest discover tests`

### GitHub
- One project repository per group
- Repository name: AirBnB_clone_v3
- Update README.md with project details and contributions

## Tasks
0. **Restart from scratch!**
   - Fork the provided codebase and make necessary updates
   - Update repository name to AirBnB_clone_v3
   - Add contributors' names and contributions to README.md

1. **Never fail!**
   - Ensure all existing tests pass
   - Add new tests to enhance test coverage

2. **Improve storage**
   - Update DBStorage and FileStorage classes with new methods
   - Implement methods to retrieve one object and count objects in storage
   - Write tests for the newly added methods

3. **Status of your API**
   - Create an endpoint to return the status of the API
   - Implement a route `/api/v1/status` to return status as JSON

4. **Some stats?**
   - Create an endpoint to retrieve the number of objects by type
   - Implement route `/api/v1/stats` to return counts of objects as JSON

5. **Not found**
   - Create a handler for 404 errors to return JSON-formatted response
   - Return status code 404 with content `"error": "Not found"`

6. **State**
   - Create view for State objects handling RESTful API actions
   - Implement endpoints for retrieving, creating, updating, and deleting states

### Task 7: City API

This API provides endpoints to manage City objects.

#### Endpoints

1. **Retrieve all cities of a state**
   - **GET** `/api/v1/states/<state_id>/cities`
     - Retrieves the list of all City objects of a State.
     - If the `state_id` is not linked to any State object, it raises a 404 error.

2. **Retrieve a city**
   - **GET** `/api/v1/cities/<city_id>`
     - Retrieves a City object.
     - If the `city_id` is not linked to any City object, it raises a 404 error.

3. **Delete a city**
   - **DELETE** `/api/v1/cities/<city_id>`
     - Deletes a City object.
     - If the `city_id` is not linked to any City object, it raises a 404 error.
     - Returns an empty dictionary with the status code 200.

4. **Create a city**
   - **POST** `/api/v1/states/<state_id>/cities`
     - Creates a City.
     - If the `state_id` is not linked to any State object, it raises a 404 error.
     - If the HTTP body request is not a valid JSON, it raises a 400 error with the message "Not a JSON".
     - If the dictionary doesn’t contain the key `name`, it raises a 400 error with the message "Missing name".
     - Returns the new City with the status code 201.

5. **Update a city**
   - **PUT** `/api/v1/cities/<city_id>`
     - Updates a City object.
     - If the `city_id` is not linked to any City object, it raises a 404 error.
     - If the HTTP request body is not valid JSON, it raises a 400 error with the message "Not a JSON".
     - Update the City object with all key-value pairs of the dictionary.
     - Ignore keys: `id`, `state_id`, `created_at`, and `updated_at`.
     - Returns the City object with the status code 200.

#### Example Usage

Retrieve all cities of a state:
```bash
curl -X GET http://0.0.0.0:5000/api/v1/states/<state_id>/cities
```

Retrieve a city:
```bash
curl -X GET http://0.0.0.0:5000/api/v1/cities/<city_id>
```

Delete a city:
```bash
curl -X DELETE http://0.0.0.0:5000/api/v1/cities/<city_id>
```

Create a city:
```bash
curl -X POST http://0.0.0.0:5000/api/v1/states/<state_id>/cities -H "Content-Type: application/json" -d '{"name": "<city_name>"}'
```

Update a city:
```bash
curl -X PUT http://0.0.0.0:5000/api/v1/cities/<city_id> -H "Content-Type: application/json" -d '{"name": "<new_city_name>"}'
```

#### Repository

- GitHub Repository: [AirBnB_clone_v3](https://github.com/Amastina1/AirBnB_clone_v3)
- Files: `api/v1/views/cities.py`, `api/v1/views/__init__.py`

### Task 13: Place - Amenity

This task involves creating a new view for managing the link between Place objects and Amenity objects.

#### File Structure

- **View File**: `api/v1/views/places_amenities.py`
- **Update**: `api/v1/views/__init__.py` to import the new file

#### Functionality

1. **Retrieve all Amenity objects of a Place**
   - **GET** `/api/v1/places/<place_id>/amenities`
     - Retrieves the list of all Amenity objects of a Place.
     - If the `place_id` is not linked to any Place object, it raises a 404 error.

2. **Delete an Amenity object from a Place**
   - **DELETE** `/api/v1/places/<place_id>/amenities/<amenity_id>`
     - Deletes an Amenity object from a Place.
     - If the `place_id` is not linked to any Place object, it raises a 404 error.
     - If the `amenity_id` is not linked to any Amenity object, it raises a 404 error.
     - If the Amenity is not linked to the Place before the request, it raises a 404 error.
     - Returns an empty dictionary with the status code 200.

3. **Link an Amenity object to a Place**
   - **POST** `/api/v1/places/<place_id>/amenities/<amenity_id>`
     - Links an Amenity object to a Place.
     - If the `place_id` is not linked to any Place object, it raises a 404 error.
     - If the `amenity_id` is not linked to any Amenity object, it raises a 404 error.
     - If the Amenity is already linked to the Place, it returns the Amenity with the status code 200.
     - Returns the Amenity with the status code 201.

#### Repository

- **GitHub Repository**: [AirBnB_clone_v3](https://github.com/Amastina1/AirBnB_clone_v3)
- **Files**: `api/v1/views/places_amenities.py`, `api/v1/views/__init__.py`

### Task 14: Security Improvements!

This task aims to improve the security of the User object by hashing passwords and updating the `to_dict()` method.

#### Files

- **BaseModel**: `models/base_model.py`
- **User**: `models/user.py`

#### Changes

1. **Update `to_dict()` Method**
   - Modify the `to_dict()` method of BaseModel to remove the password key except when used by FileStorage to save data to disk.

2. **Password Hashing**
   - Hash the password to an MD5 value each time a new User object is created or the password is updated.
   - In DBStorage, store the hashed password.
   - In FileStorage, store the hashed password.

#### Repository

- **GitHub Repository**: [AirBnB_clone_v3](https://github.com/Amastina1/AirBnB_clone_v3)
- **Files**: `models/base_model.py`, `models/user.py`

### Task 15: Search

This task involves adding a new endpoint to search for Place objects based on specific criteria.

#### Functionality

- **Endpoint**: **POST** `/api/v1/places_search`
- **JSON Body** (Optional):
  - `states`: List of State ids
  - `cities`: List of City ids
  - `amenities`: List of Amenity ids

#### Search Rules

- Validate JSON request; raise a 400 error if not valid.
- If the JSON body is empty or all key lists are empty, retrieve all Place objects.
- Include Place objects for each State id listed in states.
- Include Place objects for each City id listed in cities.
- If both states and cities are provided, results should include Place objects in every City in every State listed in states, plus every City listed individually in cities.
- If amenities list is provided, limit search results to Place objects having all listed amenities.

#### Example Usage

```bash
curl -X POST http://0.0.0.0:5000/api/v1/places_search -H "Content-Type: application/json" -d '{"states": ["<state_id_1>", "<state_id_2>"], "cities": ["<city_id_1>", "<city_id_2>"], "amenities": ["<amenity_id_1>", "<amenity_id_2>"]}'
```

#### Repository

- **GitHub Repository**: [AirBnB_clone_v3](https://github.com/Amastina1/AirBnB_clone_v3)
- **File**: `api/v1/views/places.py`

## Copyright
© 2024 ALX, All rights reserved. Plagiarism is strictly forbidden and will result in removal from the program.
