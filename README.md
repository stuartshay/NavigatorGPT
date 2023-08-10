# NavigatorGPT

## Description

NavigatorGPT is an ETL tool that leverages OpenAI's ChatGPT as a task engine. Its primary function is to generate MongoDB syntax, enabling users to import data seamlessly into a MongoDB database.

## Features

- **Dynamic MongoDB Syntax Generation**: Convert your Excel data into MongoDB-friendly syntax with minimal effort.
- **Guided Workflow**: A structured step-by-step process ensures data integrity and ease of use.
- **User-Friendly Interface**: A clear and intuitive interface powered by ChatGPT.

## Data Import Workflow

The following steps detail the MongoDB Data Import Workflow utilized by NavigatorGPT:

### 1. Start Workflow

- Generate a unique Build ID.
- Record the start timestamp.

### 2. Load Mandatory Provided Files

- GraphQL Schema Definition
- Mapping File
- Excel Data File
- Hint File (Workflow guide)

### 3. Display Excel File Information

- Display Columns in the Excel File
- Display the document Mapping Fields for each column
- Display the number of rows in the Excel file.

### 4. Excel File Validation

- Validate that all columns in the Excel file are defined in the mapping file.
- Validate that all columns in the Excel file are defined as properties anywhere in the GraphQL schema.
- Check if the Excel file has any extra columns not defined in the mapping file or GraphQL schema.
- If 'id' column exists in the Excel, validate IDs as 24-character hexadecimal strings mapping file enforces this rule.

### 5. Data Processing

- Process the Excel data according to the mapping file.
- Validate data types based on the mapping file.
- Apply any special rules or transformations defined in the mapping file.
- For each validation:
  - Display a ✅ icon if the validation is successful.
  - Display a ❌ icon if the validation fails.

### 6. Output Results

- Generate a JavaScript array based on the processed Excel data and the provided template.
- Adjust the template structure to ensure the output matches the desired JavaScript array format.
- Provide a summary of the processed data, including counts, any issues, and a preview of the formatted array.
- Provide a link for downloading the complete formatted array. (The File Should end in mm-dd-yyyy.hh.mm.ss.json)

### 7. End Workflow

- Record the end timestamp.
- Calculate and display the total time taken for the entire workflow.

## Installation

(Provide steps for setting up the project locally. This might include cloning the repository, installing dependencies, and any other necessary configurations.)

## Contributing

We welcome contributions to NavigatorGPT! Whether it's bug reports, feature suggestions, or direct contributions to the code, all are appreciated. For direct contributions, please fork the repository, make your changes, and submit a pull request.

## License

(Provide license information here. If you're using a standard license, like MIT or Apache, you can directly state that here.)

## Acknowledgments

- OpenAI and the ChatGPT team for their invaluable tool that powers dynamic data processing.
- All contributors and users who help in refining and expanding the capabilities of NavigatorGPT.

## Features

- **Dynamic MongoDB Syntax Generation**: Convert your Excel data into MongoDB-friendly syntax with ease.
- **Comprehensive Database**: Aiming to cover every NYC landmark, attraction, and monument.
- **User-Friendly Interface**: Simple upload process guided by ChatGPT.

## Installation

(Provide steps for setting up the project locally. This might include cloning the repository, installing dependencies, and any other necessary configurations.)

## Usage

1. Navigate to the main interface.
2. Upload your Excel file containing NYC landmark, attraction, or monument data.
3. Let ChatGPT process the data and generate the MongoDB syntax.
4. Use the provided syntax to import data into your MongoDB instance.

## Contributing

We welcome contributions to NavigatorGPT! Whether it's bug reports, feature suggestions, or direct contributions to the code, all are appreciated. For direct contributions, please fork the repository, make your changes, and submit a pull request.

## License

(Provide license information here. If you're using a standard license, like MIT or Apache, you can directly state that here.)

## Acknowledgments

- OpenAI and the ChatGPT team for providing the backbone of the dynamic data processing.
- All contributors and users who are helping to make this database more comprehensive.
