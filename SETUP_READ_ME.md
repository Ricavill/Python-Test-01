
# How to Run the Application

## 1. Clone the Project
Clone the repository using the following command:

```sh
git clone https://github.com/Ricavill/Python-Test-01.git
```

## 2. Configure Environment Variables
Add values to the environment variables inside the `.env` file.  
For the database route variable, write it like this in order to use SQLite:

```env
DATABASE_URL=sqlite:///mi_base_de_datos.db
```

## 3. Build and Run the Application
Execute the following commands:

```sh
docker compose build --no-cache
docker compose up
```

> **Note:** If there are errors while installing `numpy`, try installing C++ and C development tools from the [official Microsoft page](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

---

# API Usages

## **Login**
**Method:** `POST`  
**Endpoint:**  
```sh
http://<rooturl>:8000/api/users/login
```
**Body Example (JSON):**
```json
{
  "email": "your_email",
  "password": "your_password"
}
```

---

## **Ingest (Load Up Tweet Database)**
**Method:** `POST`  
**Endpoint:**  
```sh
http://<rooturl>:8000/api/tweets/ingest
```

---

## **Insights**
**Method:** `GET`  
**Endpoint:**  
```sh
http://<rooturl>:8000/api/companies/{company_id}/insights
```

---

## **AI Insights**
**Method:** `GET`  
**Endpoint:**  
```sh
http://<rooturl>:8000/api/companies/{company_id}/ai-insights
```

---

## **API Documentation**
To see all available endpoints, visit:  
```sh
http://<rooturl>:8000/documentation#/
