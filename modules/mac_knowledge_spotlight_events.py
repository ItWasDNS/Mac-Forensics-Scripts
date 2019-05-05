"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7 on macOS
    Description: Parse knowledgeC.db for Spotlight viewer events:
     - Application opened (If accessed directly)
     - Type of file (Such as DOCUMENTS, PRESENTATIONS, PDF, SOURCE, OTHER)
     - Directories (DIRECTORIES)
     - Dictionary Searches (MENU_DEFINITION)
     - News (Via Browser)
"""

import os
import sqlite3

query = """
SELECT
  Z_PK AS "ZOBJECT TABLE ID",
  ZVALUESTRING as "SPOTLIGHT EVENT OBJECT",
  CASE ZSTARTDAYOFWEEK
    WHEN "1" THEN "Sunday"
    WHEN "2" THEN "Monday"
    WHEN "3" THEN "Tuesday"
    WHEN "4" THEN "Wednesday"
    WHEN "5" THEN "Thursday"
    WHEN "6" THEN "Friday"
    WHEN "7" THEN "Saturday"
  END "DAY OF WEEK",
  DATETIME(ZSTARTDATE+978307200,'UNIXEPOCH') as "START",
  ZSECONDSFROMGMT/3600 AS "GMT OFFSET"
FROM ZOBJECT
  WHERE ZSTREAMNAME 
    IS 'com.apple.spotlightviewer.events';
"""
summary = """--
ZOBJECT Table PK: %s
Spotlight Entity: %s
Day of Week: %s
Date Searched: %s (%s)
"""


def process_spotlight(db, output_path):
    """ Process knowledgeC for Spotlight Interactions """
    # Query Database
    try:
        conn = sqlite3.connect(db)
        answer = conn.execute(query).fetchall()
        conn.close()
    except sqlite3.OperationalError as e:
        print("Error: %s" % str(e))
        return None

    # Generate Output
    with open(os.path.join(output_path, 'knowledge_spotlight_events.txt'), 'w') as o:
        for name in answer:
            o.write(summary % name)


if __name__ == '__main__':
    from helpers.mac_path_handler import process_directory_paths
    database, out_path = process_directory_paths()
    process_spotlight(database, out_path)
else:
    from modules.helpers.mac_path_handler import process_directory_paths
