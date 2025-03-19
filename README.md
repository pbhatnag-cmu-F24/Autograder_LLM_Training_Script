# Autograder_Dataset_Processing_Pipeline
```

To run the application, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/pbhatnag-cmu-F24/Autograder_Dataset_Processing_Pipeline.git
```

2. Change to the project directory:
```bash
cd path/to/Autograder_Dataset_Processing_Pipeline
```

3. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Start the application:
```bash
python app.py
```

6. Open your web browser and navigate to `http://localhost:5000` or use an API platform like Postman.

7. Use the provided cURL commands to interact with the API.

This project utilizes the following cURL commands:

1. Unzip API:
```bash
curl --location 'http://127.0.0.1:5000/api/unzip' \
--form 'file=@"postman-cloud:///1f004925-dcdf-4380-81b1-8e200809e3ba"'
```

2. File Extension Filter API:
```bash
curl --location 'http://127.0.0.1:5000/api/filter/fileext' \
--header 'Content-Type: application/json' \
--data '{"filter_type": "in", "filter_list": [".java", ".md"]} '
```

3. Filename Filter API:
```bash
curl --location 'http://127.0.0.1:5000/api/filter/filename' \
--header 'Content-Type: application/json' \
--data '{"filter_type": "out", "filter_list": ["Main.java", "DatabaseDriver.java", "PostgresDriver.java", "README.md"]}'
```

4. Dataset Extraction API:
```bash
curl --location 'http://127.0.0.1:5000/api/dataset/extraction' \
--header 'Content-Type: application/json' \
--data '{"division": "method"} '
```

5. Dataset Processing API:
```bash
curl --location 'http://127.0.0.1:5000/api/dataset/process' \
--header 'Content-Type: application/json' \
--data '{
           "dataset_division": "method",
           "filter_type": "out",
           "filter_list": ["getId", "setId", "getUsername", "setUsername", "getAge", "setAge", "toString"]
         }'
```
