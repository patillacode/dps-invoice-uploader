# Automatic Invoice Uploader

## Custom invoice uploader for DPS API

### Setup

You can either run the make command for an automatic setup:

```bash
# Clone this repo
$ git clone git@github.com:patillacode/dps-invoice-uploader.git

# Enter the project folder
$ cd dps-invoice-uploader

# Run the following command
$ make install
```

or for a more manual process do the following:

```bash
# Clone this repo
$ git clone git@github.com:patillacode/dps-invoice-uploader.git

# Enter the project folder
$ cd dps-invoice-uploader

# Create a virtual environment
$ python3 -m venv venv

# Activate your newly created virtual environment
$ source venv/bin/activate

# Install all necessary dependencies
$ pip install -r requirements.txt

# Copy the secrets sample file into a secrets.py file
$ cp secrets.sample.py secrets.py
```

_Note: Remember to fill the `secrets.py` file with the proper values._

### Usage

```text
usage: dps_api.py [-h] -f FILE_PATH -ft FILE_TYPE -it INVOICE_TYPE -d DATE [-b BANK_NAME] [-fn FILE_NAME] [-desc DESCRIPTION] [-in INVOICE_NUMBER] [--debug] [--test]

Arguments:
  -h, --help            show this help message and exit

  -f FILE_PATH, --file-path FILE_PATH
                        Path to invoice file

  -ft FILE_TYPE, --file-type FILE_TYPE
                        One of: "image/png" | "application/pdf" | "application/vnd.ms-excel"

  -it INVOICE_TYPE, --invoice-type INVOICE_TYPE
                        One of "emitida" | "recibida" | "extracto"

  -d DATE, --date DATE
                        Date within the correct trimester in YYYY-MM-DD format

  -b BANK_NAME, --bank-name BANK_NAME
                        Only for bank statements (extracto), see the following allowed values: ['BANCO CAMINOS', 'BANKIA', 'BANKINTER',
                        'BBVA', 'CAIXA', 'IBERCAJA', 'ING DIRECT', 'SABADELL', 'SANTANDER', 'TRIODOS BANK']

  -fn FILE_NAME, --file-name FILE_NAME
                        If not specified it will be the given file's name

  -desc DESCRIPTION, --description DESCRIPTION
                        For internal reference.

  -in INVOICE_NUMBER, --invoice-number INVOICE_NUMBER
                        For internal reference.

  --debug               Enable to print out the response
  --test                To test with a dummy example.
```

### Example

```bash
$ python dps_api.py --test

        URL: https://your.api.server.domain/your/api/server/endpoint
        Status Code: 200
        JSON Response: {'ids': [{'id': 25289}], 'repetidas': []}

```
