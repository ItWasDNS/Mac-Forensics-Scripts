"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7 on macOS
    Description: Retrieves entities parsed from the following applications:
     - com.apple.Maps
     - com.apple.MobileSMS
     - com.apple.iChat
     - com.apple.mobilesafari
     - com.yelp.yelpiphone
"""

import os
import sqlite3

# Fix Query for Presentation
query = """
SELECT
  ZOBJECT.Z_PK AS "ZOBJECT TABLE ID",
  ZSOURCE.ZBUNDLEID AS "BUNDLE ID",
  ZSTRUCTUREDMETADATA.Z_CDENTITYMETADATAKEY__NAME AS "ENTITY EXTRACTED",
  CASE ZOBJECT.ZSTARTDAYOFWEEK
    WHEN "1" THEN "Sunday"
    WHEN "2" THEN "Monday"
    WHEN "3" THEN "Tuesday"
    WHEN "4" THEN "Wednesday"
    WHEN "5" THEN "Thursday"
    WHEN "6" THEN "Friday"
    WHEN "7" THEN "Saturday"
  END "DAY OF WEEK",
  DATETIME(ZOBJECT.ZSTARTDATE+978307200,'UNIXEPOCH') as "START",
  ZOBJECT.ZSECONDSFROMGMT/3600 AS "GMT OFFSET",
  Z_CDPORTRAITMETADATAKEY__OSBUILD
FROM
  ZOBJECT
    LEFT JOIN
      ZSTRUCTUREDMETADATA
        ON ZOBJECT.ZSTRUCTUREDMETADATA = ZSTRUCTUREDMETADATA.Z_PK
    LEFT JOIN
      ZSOURCE
        ON ZOBJECT.ZSOURCE = ZSOURCE.Z_PK
  WHERE
    ZSTREAMNAME IS "/portrait/entity";
"""
summary = """--
ZOBJECT Table PK: %s
Source: %s
Entity: %s
Day of Week: %s
Date Searched: %s (%s)
Device OS: %s
"""


def process_entities(db, output_path):
    """ Process knowledgeC for Entities """
    # Query Database
    try:
        conn = sqlite3.connect(db)
        answer = conn.execute(query).fetchall()
        conn.close()
    except sqlite3.OperationalError as e:
        print("Error: %s" % str(e))
        return None

    # Generate Output
    with open(os.path.join(output_path, 'knowledge_entities.txt'), 'w') as o:
        for name in answer:
            o.write(summary % name)


if __name__ == '__main__':
    from helpers.mac_path_handler import process_directory_paths
    database, out_path = process_directory_paths()
    process_entities(database, out_path)
else:
    from modules.helpers.mac_path_handler import process_directory_paths
