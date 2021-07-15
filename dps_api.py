# python dps_api.py -f ~/Downloads/cv-3.pdf -ft application/pdf -it recibida -d 2021-07-01 --debug
import argparse
import pathlib
import sys
from datetime import datetime
from secrets import DPS_API_INVOICE_UPLOAD_ENDPOINT, DPS_API_SERVER, DPS_API_TOKEN

import requests

BANK_LIST = [
    'BANCO CAMINOS',
    'BANKIA',
    'BANKINTER',
    'BBVA',
    'CAIXA',
    'IBERCAJA',
    'ING DIRECT',
    'SABADELL',
    'SANTANDER',
    'TRIODOS BANK',
]


def test():
    url = f'{DPS_API_SERVER}{DPS_API_INVOICE_UPLOAD_ENDPOINT}'

    payload = {
        'tipo': 'emitida',
        'fecha': '2021-07-01',
        'nombre': 'Testing DPS API',
        'numeroFactura': '333',
        'descripcion': 'prueba',
        'banco': 'BBVA',
    }

    files = [
        (
            'file',
            (
                'TEST.pdf',
                open('./TEST.pdf', 'rb'),
                'application/pdf',
            ),
        )
    ]

    headers = {
        'Authorization': DPS_API_TOKEN,
    }
    response = requests.post(url, headers=headers, data=payload, files=files)
    print(
        f'''
        URL: {url}
        Status Code: {response.status_code}
        JSON Response: {response.json()}
        '''
    )


def upload_invoice(
    file_path,
    file_type,
    invoice_type,
    date,
    bank_name=None,
    file_name=None,
    description=None,
    invoice_number=None,
):
    url = f'{DPS_API_SERVER}{DPS_API_INVOICE_UPLOAD_ENDPOINT}'

    mandatory_payload = {
        'tipo': invoice_type,
        'fecha': date,
    }

    optional_payload = {}

    if invoice_type == 'extracto':

        if not bank_name:
            print('For Bank Statements the bank parameter need to be provided.')
            return False

        elif bank_name not in BANK_LIST:
            print('Bank parameter has to be one of the following:', BANK_LIST)
            return False

        optional_payload = {'banco': bank_name}

    if file_name:
        optional_payload.update({'nombre': file_name})

    if description:
        optional_payload.update({'descripcion': description})

    if invoice_number:
        optional_payload.update({'numeroFactura': invoice_number})

    payload = {**mandatory_payload, **optional_payload}

    files = [
        (
            'file',
            (
                file_name or pathlib.Path(file_path).name,
                open(file_path, 'rb'),
                file_type,
            ),
        )
    ]

    headers = {
        'Authorization': DPS_API_TOKEN,
    }
    response = requests.post(url, headers=headers, data=payload, files=files)
    json_response = response.json()

    if response.status_code == 200:
        if json_response['repetidas']:
            print(
                'It seems like this file was already uploaded, please check your input '
                'or go to https://gaudium.dpsconsulting.es/facturas/ select the correct '
                'trimester and verify.'
            )
            return False
    else:
        print(f'Something went wrong: \n\t {response.json()} ({response.status_code})')
        return False

    return json_response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatic Invoice Uploader')

    parser.add_argument(
        '-f',
        '--file-path',
        dest='file_path',
        required='--test' not in sys.argv,
        help='Path to invoice file',
    )

    parser.add_argument(
        '-ft',
        '--file-type',
        dest='file_type',
        required='--test' not in sys.argv,
        help='One of: "image/png" | "application/pdf" | "application/vnd.ms-excel"',
    )

    parser.add_argument(
        '-it',
        '--invoice-type',
        dest='invoice_type',
        required='--test' not in sys.argv,
        help='One of "emitida" | "recibida" | "extracto"',
    )

    parser.add_argument(
        '-d',
        '--date',
        dest='date',
        type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
        required='--test' not in sys.argv,
        help='Date within the correct trimester in YYYY-MM-DD format',
    )

    parser.add_argument(
        '-b',
        '--bank-name',
        dest='bank_name',
        default=None,
        help=(
            'Only for bank statements (extracto), see the following allowed values: '
            f'\n{BANK_LIST}'
        ),
    )

    parser.add_argument(
        '-fn',
        '--file-name',
        dest='file_name',
        default=None,
        help='If not specified it will be the given file\'s name',
    )

    parser.add_argument(
        '-desc',
        '--description',
        dest='description',
        default=None,
        help='For internal reference.',
    )

    parser.add_argument(
        '-in',
        '--invoice-number',
        dest='invoice_number',
        default=None,
        help='For internal reference.',
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable to print out the response',
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='To test with a dummy example.',
    )

    args = parser.parse_args()

    if args.test:
        test()
    else:
        upload = upload_invoice(
            file_path=args.file_path,
            file_type=args.file_type,
            invoice_type=args.invoice_type,
            date=args.date,
            bank_name=args.bank_name,
            file_name=args.file_name,
            description=args.description,
            invoice_number=args.invoice_number,
        )

        if upload:
            print('Invoice uploaded!')
            if args.debug:
                print(upload)
        else:
            print('Please check the message above, something didn\'t work as expected!')
