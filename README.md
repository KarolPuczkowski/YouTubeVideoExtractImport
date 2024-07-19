## Magento 2 Python Module for YouTube Video Import

This module allows you to extract YouTube video data and import it into the product media gallery in Magento 2.

### Requirements

- **Python 3**: Ensure Python 3 is installed on your system.
- **mysql-connector-python**: A MySQL database connector for Python.
- **python-dotenv**: A Python library to manage environment variables.

### .env File Structure

Below is the structure for the `.env` file used by the module. This file contains database connection details for both extraction and import processes.

```dotenv
# Extraction Database Configuration
EXTRACT_DB_NAME=""
EXTRACT_DB_HOST=""
EXTRACT_DB_USER=""
EXTRACT_DB_PASSWORD=""

# Import Database Configuration
IMPORT_DB_NAME=""
IMPORT_DB_HOST=""
IMPORT_DB_USER=""
IMPORT_DB_PASSWORD=""
```
