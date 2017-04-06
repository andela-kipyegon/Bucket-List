
[![CircleCI](https://circleci.com/gh/andela-kipyegon/Bucket-List/tree/develop.svg?style=svg)](https://circleci.com/gh/andela-kipyegon/Bucket-List/tree/develop)

[![Coverage Status](https://coveralls.io/repos/github/andela-kipyegon/Bucket-List/badge.svg?branch=develop)](https://coveralls.io/github/andela-kipyegon/Bucket-List?branch=develop)

# Bucket-List
It is a list of all the goals you want to achieve, dreams you want to fulfill and life experiences you desire to experience before you die.

All Endpoints:

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v1/auth/register` |  Register a user. |
|POST| `/api/v1/auth/login` | Login user.|
|POST| `/api/v1/bucketlists/` | Create a new bucket list. |
|GET| `/api/v1/bucketlists/` | Retrieve all the created bucket lists. |
|GET| `/api/v1/bucketlists/<bucket_id>` | Get a single bucket list. |
|PUT| `/api/v1/bucketlists/<bucket_id>` | Update a single bucket list. |
|DELETE| `/api/v1/bucketlists/<bucket_id>` | Delete single bucket list. |
|POST| `/api/v1/bucketlists/<bucket_id>/items `| Add a new item to this bucket list. |
|PUT|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Update this bucket list. |
|DELETE|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Delete this single bucket list. |
|GET| `/api/v1/bucketlists?per_page=10&page=1` | Pagination to get 10 bucket list records.|
|GET| `/api/v1/bucketlists?q=a bucket` | Search for bucket lists with name like a bucket. |

**Login User**
----
  Returns json data about a single user.

* **URL**

  `api/<version>/auth/login`

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
   `version=[string]`

* **Data Params**
  ```
  email=[string]

  password=[string]
  ```

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** <br />
    ```
    {
      "auth_token": "token",
      "first_name": "oliver",
      "last_name": "munala",
      "message": "Successfully logged in.",
      "status": "success"
    }
    ```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** <br />
     ```
     {
        "message": "Invalid user or Password mismatch.",
        "status": "fail"
     }
     ```

  OR

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** <br />
      ```
      {
        "status": "fail",
        "message": "Try again"
      }
      ```

* **Sample Call:**

   * **api/v1/auth/login**<br />

     **Payload:**

      ```
      {
          "email":"olivermnala@gmail.com",
          "password":"password"
      }
      ```
  ----

  **Register User**
  ----
* **URL**

  `api/<version>/auth/register`

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
   `version=[string]`

* **Data Params**
  ```
  first_name=[string]

  last_name=[string]

  email=[string]

  password=[string]
  ```

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** <br />
    ```
    {
      "auth_token": "token",
      "message": "Successfully logged in.",
      "status": "success"
    }
    ```
 
* **Error Response:**

  * **Code:** 202 ACCEPTED <br />
    **Content:** <br />
    ```
    {
      "message": "User already exists. Please Log in.",
      "status": "fail"
    }
    ```

  OR

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** <br />
    ```
    {
      "status": "fail",
      "message": "Try again"
    }
    ```

* **Sample Call:**

   * **api/v1/auth/register**<br />

     **Payload:**

      ```
      {   
          "first_name": "oliver",
          "last_name": "munala",
          "email":"olivermnala@gmail.com",
          "password":"password"
      }
      ```
  ----

  **Create bucketlist**
  ----
* **URL**

  `api/<version>/bucketlist`

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
   None

* **Data Params**

  ```
  name=[string]
  ```


* **Success Response:**

  * **Code:** 201 <br />
    **Content:**
     ```
     {
        "created_at": "Thu, 30 Mar 2017 22:51:29 -0000",
        "created_by": "1",
        "id": 3,
        "items": [],
        "name": "India",
        "updated_at": "Thu, 30 Mar 2017 22:51:29 -0000",
        "uri": "/api/v1/bucketlist/3"
      }
      ```
    
 
* **Error Response:**

  * **Code:** 202 ACCEPTED <br />
    **Content:** <br />

     ```
     { "message": "bucketlist India already exists"}
     ```


* **Sample Call:**

   * **api/v1/bucketlist**<br />

     **Payload:**

      ```
      {   
          "name": "Travel"
      }
      ```
   ----

  **Fetch bucketlist(s)**
  ----
* **URL**

  `api/<version>/bucketlist/`

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]
   ```

   **Optional:**
   ```
   q=[string]

   page=[page]

   per_page=[per_page]
   ```

* **Data Params**

  None


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    ```
    {
      "bucketlist": [
    {
        "created_at": "Wed, 29 Mar 2017 20:55:03 -0000",
        "created_by": "1",
        "id": 1,
        "items": [],
        "name": "India",
        "updated_at": "Wed, 29 Mar 2017 20:55:03 -0000",
        "uri": "/api/v1/bucketlist/1"
    }],
      "meta": {
        "next_page": "Null",
        "previous_page": "Null",
        "total_pages": 1
      }
    }
    ```

   OR

  * **Code:** 200 OK <br />
    **Content:** <br />
    
    ```
    {'message': 'no bucket_list available'}
    ```
    
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** <br />

     `UNAUTHORIZED`


* **Sample Call:**

   * **api/v1/bucketlist/**<br />
   ----

  **Fetch bucketlist**
  ----
* **URL**

  `api/<version>/bucketlist/<id>`

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]

   id=[integer]
   ```

* **Data Params**

  None


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    ```
    {
        "created_at": "Wed, 29 Mar 2017 20:55:03 -0000",
        "created_by": "1",
        "id": 1,
        "items": [],
        "name": "India",
        "updated_at": "Wed, 29 Mar 2017 20:55:03 -0000",
        "uri": "/api/v1/bucketlist/1"
    }
    ```
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** <br />

     `UNAUTHORIZED`
  
  OR

  * **Code:** 404 RESOURCE NOT FOUND <br />
    **Content:** <br />
    
    ```
    {'error':'bucket list does not exist'}
    ```


* **Sample Call:**

   * **api/v1/bucketlist/1**<br />

  ----

  **Update bucketlist**
  ----
* **URL**

  `api/<version>/bucketlist/<id>`

* **Method:**

  `PUT`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]

   id=[integer]
   ```

* **Data Params**

   ```
   name=[string]
   ```


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />
    ```
    {
      "created_at": "Thu, 30 Mar 2017 22:51:29 -0000",
      "created_by": "1",
      "id": 3,
      "items": [],
      "name": "Nepal",
      "updated_at": "Fri, 31 Mar 2017 07:56:33 -0000",
      "uri": "/api/v1/bucketlist/3"
    }
    ```
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** <br />

     `UNAUTHORIZED`
  
  OR

  * **Code:** 404 RESOURCE NOT FOUND <br />
    **Content:** <br />
    
    ```
    {'error':'bucket list does not exist'}
    ```


* **Sample Call:**

   * **api/v1/bucketlist/1**<br />

  ----

  **Delete bucketlist**
  ----
* **URL**

  api/\<version>/bucketlist/\<id>

* **Method:**

  `DELETE`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]

   id=[integer]
   ```

* **Data Params**

   None


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br />

    ```
    {"message": "bucket list Nepal deleted successfully"}
    ```
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** <br />

     `UNAUTHORIZED`
  
  OR

  * **Code:** 404 RESOURCE NOT FOUND <br />
    **Content:** <br />
    
    ```
    {'error':'bucket list does not exist'}
    ```


* **Sample Call:**

   * **api/v1/bucketlist/1**<br />

 ----

  **Create bucketlist item**
  ----
* **URL**

  `api/<version>/bucketlist/<id>/bucketlistitem/`

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]

   bucketlist_id=[integer]
  
   bucketlist_item_id=[integer]
   ```
   

* **Data Params**
   ```
   item_name=[string]
   ```


* **Success Response:**

  * **Code:** 201 <br />
    **Content:**  <br />
     ```
     {
       "bucketlist_item_id": 1,
       "created_at": "Fri, 31 Mar 2017 08:13:51 -0000",
       "done": "False",
       "name": "India",
       "updated_at": "Fri, 31 Mar 2017 08:13:51 -0000"
    }
       ```
    
 
* **Error Response:**

  * **Code:** 202 ACCEPTED <br />
    **Content:** <br />

     ```
     {"message": "item already exists"}
     ```


* **Sample Call:**

   * **api/v1/bucketlist/1/bucketlistitem/**<br />

     **Payload:**

      ```
      { "item_name": "Taj Mahal"}
      ```
   ----

  **Update bucketlist item**
  ----
* **URL**

  `api/\<version>/bucketlist/\<id>/bucketlistitem/\<id>`

* **Method:**

  `PUT`
  
*  **URL Params**

   **Required:**
   ```
   version=[string]

   bucketlist_id=[integer]
  
   bucketlist_item_id=[integer]
   ```

* **Data Params**
   
   **Optional:**
  ```
   item_name=[string]

   done=[boolean]
  ```


* **Success Response:**

  * **Code:** 201 <br />
    **Content:**  <br />
     ```
     {
       "bucketlist_item_id": 1,
       "created_at": "Fri, 31 Mar 2017 08:13:51 -0000",
       "done": "False",
       "name": "India",
       "updated_at": "Fri, 31 Mar 2017 08:13:51 -0000"
    }
       ```
    
 
* **Error Response:**

  * **Code:** 202 ACCEPTED <br />
    **Content:** <br />

     ```
     {"message": "item already exists"}
     ```


* **Sample Call:**

   * **api/v1/bucketlist/1/bucketlistitem/1**<br />

     **Payload:**

      ```
      {"item_name": "Taj Mahal"}
      ```
     ----

  **Delete bucketlist item**
  ----
* **URL**

  `api/<version>/bucketlist/<id>/bucketlistitem/<id>`

* **Method:**

  `DELETE`
  
*  **URL Params**

   **Required:**
 
   ```
   version=[string]

   bucketlist_id=[integer]
  
   bucketlist_item_id=[integer]
   ```

* **Data Params**
   
   None


* **Success Response:**

  * **Code:** 201 <br />
    **Content:**  <br />
    ```
    {"message": "bucket list item deleted"}
    ```
    
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** <br />

     ```
     { "message": "bucket list item does not exist"}
     ```


* **Sample Call:**

   * **api/v1/bucketlist/1/bucketlistitem/1**<br />

 
