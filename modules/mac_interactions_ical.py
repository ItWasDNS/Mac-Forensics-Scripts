"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7 on macOS
    Description: Parse interactionsC.db for iCal information
"""

import os
import sqlite3

query = """
SELECT
  ZINTERACTIONS.Z_PK,
  ZKEYWORDS.ZKEYWORD,
  DATETIME(ZINTERACTIONS.ZSTARTDATE + 978307200, 'unixepoch')
    AS "CALENDAR START TIME",
  DATETIME(ZINTERACTIONS.ZENDDATE + 978307200, 'unixepoch')
    AS "CALENDAR END TIME",
  ZINTERACTIONS.ZUUID
FROM
  ZINTERACTIONS
  LEFT JOIN Z_3KEYWORDS
    ON ZINTERACTIONS.Z_PK = Z_3KEYWORDS.Z_3INTERACTIONS1
  LEFT JOIN ZKEYWORDS
      ON Z_3KEYWORDS.Z_4KEYWORDS = ZKEYWORDS.Z_PK
  WHERE "ZBUNDLEID" IS 'com.apple.iCal';
"""

summary = """---
ZINTERACTIONS Primary Key: %s 
Calendar Event Keywords: %s
Calendar Event Start Time: %s
Calendar Event End Time: %s
Calendar Event UUID: %s
"""


def process_ical(db, output_path):
    """ Process interactionsC for iMessage and Contacts details """
    # Query Database
    try:
        conn = sqlite3.connect(db)
        answer = conn.execute(query).fetchall()
        conn.close()
    except sqlite3.OperationalError as e:
        print("Error: %s" % str(e))
        return None

    # Process Query Results
    calendar_events = {}
    with open(os.path.join(output_path, 'interactions_ical.txt'), 'w') as o:
        for result in sorted(answer, key=lambda x: x[0]):
            if result[0] in calendar_events.keys():
                calendar_events[result[0]].append(result[1])
            else:
                calendar_events[result[0]] = [result[1]]
        current = sorted(calendar_events.keys())[0]
        for result in sorted(answer, key=lambda x: x[0]):
            # Ensure each event is only output once
            if current != result[0]:
                output = summary % (result[0],
                                    calendar_events[result[0]],
                                    result[2],
                                    result[3],
                                    result[4])
                o.write(output)
                current = result[0]


if __name__ == '__main__':
    from helpers.mac_path_handler import process_directory_paths
    database, out_path = process_directory_paths()
    process_ical(database, out_path)
else:
    from modules.helpers.mac_path_handler import process_directory_paths
