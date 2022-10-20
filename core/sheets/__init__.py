# sheets.py

from __future__ import print_function
from .auth import spreadsheet_service
from .auth import drive_service


def create():
    spreadsheet_details = {"properties": {"title": "Ponto-Labsoft"}}
    sheet = (
        spreadsheet_service.spreadsheets()
        .create(body=spreadsheet_details, fields="spreadsheetId")
        .execute()
    )
    sheetId = sheet.get("spreadsheetId")

    permission1 = {
        "type": "user",
        "role": "writer",
        "emailAddress": "jn5.guape@gmail.com",
    }
    drive_service.permissions().create(fileId=sheetId, body=permission1).execute()
    return sheetId


def read_range():
    range_name = "Sheet1!A1:D1"
    spreadsheet_id = "1EC8QDXzIkqgncwYMH8ZbElmlK1zCGqtB_mhCgP6GVeE"
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])
    print("{0} rows retrieved.".format(len(rows)))
    print("{0} rows retrieved.".format(rows))
    return rows


def write_range():
    spreadsheet_id = create()

    print("Spreadsheet ID: {0}".format(spreadsheet_id))

    range_name = "Sheet1!A1:D1"
    values = read_range()
    value_input_option = "USER_ENTERED"
    body = {"values": values}
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print("{0} cells updated.".format(result.get("updatedCells")))


def read_ranges():
    write_range()
    sheetId = "1EC8QDXzIkqgncwYMH8ZbElmlK1zCGqtB_mhCgP6GVeE"

    range_names = ["Sheet1!A2:D62"]
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=sheetId, ranges=range_names)
        .execute()
    )
    ranges = result.get("valueRanges", [])
    print("{0} ranges retrieved.".format(len(ranges)))
    return ranges


def write_ranges():
    values = read_ranges()

    spreadsheet_id = "1EC8QDXzIkqgncwYMH8ZbElmlK1zCGqtB_mhCgP6GVeE"

    data = [
        {"range": "Sheet1!A2:D21", "values": values[0]["values"]},
        {"range": "Sheet1!A22:D42", "values": values[1]["values"]},
    ]
    body = {"valueInputOption": "USER_ENTERED", "data": data}
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    print("{0} cells updated.".format(result.get("totalUpdatedCells")))


def append():
    values = read_ranges()

    spreadsheet_id = "1EC8QDXzIkqgncwYMH8ZbElmlK1zCGqtB_mhCgP6GVeE"

    data = [values[0]["values"], values[1]["values"]]
    body = {"valueInputOption": "USER_ENTERED", "data": data}
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .append(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    print("{0} cells updated.".format(result.get("totalUpdatedCells")))

def insert_row(values : list) -> int:
    spreadsheet_id = "1EC8QDXzIkqgncwYMH8ZbElmlK1zCGqtB_mhCgP6GVeE"

    total_values = read_ranges()[0]

    size = 0

    if "values" in total_values:
        total_values = total_values["values"]
        size = len(total_values)

    else:
        size = 0

    body = {"values": [values]}
    result = (
        spreadsheet_service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            body=body,
            range=f"Sheet1!A{size+2}:D{size+2}",
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )
    print("{0} cells updated.".format(result.get("updatedCells")))

    return result.get("updatedCells")


#create()
#write_ranges()