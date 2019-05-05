"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7 on macOS
    Description: Parse interactionsC.db for iMessages and Contacts information
"""

import os
import sqlite3

query_ZINTERACTIONS = """
SELECT
  ZCONTACTS.ZDISPLAYNAME,
  ZCONTACTS.ZIDENTIFIER,
  ZINTERACTIONS.ZDIRECTION,
  ZINTERACTIONS.ZISRESPONSE,
  ZINTERACTIONS.ZMECHANISM,
  ZINTERACTIONS.ZRECIPIENTCOUNT,
  DATETIME(ZINTERACTIONS.ZSTARTDATE + 978307200, 'unixepoch') AS "START DATE",
  ZINTERACTIONS.ZDOMAINIDENTIFIER,
  ZINTERACTIONS.Z_PK AS "ZINTERACTIONS TABLE ID",
  ZINTERACTIONS.ZBUNDLEID
FROM
  ZINTERACTIONS
  LEFT JOIN
    ZCONTACTS 
      ON ZINTERACTIONS.ZSENDER = ZCONTACTS.Z_PK
WHERE 
  ZINTERACTIONS.ZBUNDLEID IS 'com.apple.iChat';
"""

query_ZCONTACTS = """
SELECT
  ZDISPLAYNAME,
  ZIDENTIFIER,
  ZOUTGOINGRECIPIENTCOUNT AS "MESSAGES SENT TO CONTACT",
  ZINCOMINGSENDERCOUNT AS "MESSGES RECEIVED FROM CONTACT",
  DATETIME(ZFIRSTOUTGOINGRECIPIENTDATE + 978307200, 'unixepoch') AS "FIRST MESSAGE SENT TO CONTACT",
  DATETIME(ZFIRSTINCOMINGSENDERDATE + 978307200, 'unixepoch') AS "FIRST MESSAGE RECEIVED FROM CONTACT",
  DATETIME(ZLASTOUTGOINGRECIPIENTDATE + 978307200, 'unixepoch') AS "LAST MESSAGE SENT TO CONTACT",
  DATETIME(ZLASTINCOMINGSENDERDATE + 978307200, 'unixepoch') AS "LAST MESSAGE RECEIVED FROM CONTACT",
  ZPERSONIDTYPE,
  ZCONTACTS.Z_PK
FROM ZCONTACTS;
"""
summary = """
Contact Name: %s
Contact Phone Number: %s
# of Messages Sent to Contact: %s
# of Messages Received from Contact: %s
Time of First Message Sent to Contact: %s
Time of First Message Received from Contact: %s
Time of Last Message Sent to Contact: %s
Time of Last Message Received from Contact: %s

"""


def process_phone(number):
    """ Process Phone Number for Printing (Currently works for USA Numbers) """
    if len(number) == 12 and number[0:2] == '+1':
        return '+1(%s)%s-%s' % (number[2:5], number[5:8], number[8:12])
    else:
        return number


def process_interactions(db, output_path):
    """ Process interactionsC for iMessage and Contacts details """
    # Query Database
    try:
        conn = sqlite3.connect(db)
        answer_contacts = conn.execute(query_ZCONTACTS).fetchall()
        answer_interactions = conn.execute(query_ZINTERACTIONS).fetchall()
        conn.close()
    except sqlite3.OperationalError as e:
        print("Error: %s" % str(e))
        return None

    # Generate Contact Dictionary
    contacts = {}
    for interaction in answer_interactions:
        ident = interaction[0]
        num = interaction[1]
        if ident is not None and num is not None:
            contacts[num] = ident

    # Generate Output (Summary/Detailed)
    with open(os.path.join(output_path, 'interactions_imessage.txt'), 'w') as o:
        for result in sorted(answer_contacts, key=lambda x: x[0]):
            if result[8] == 3:
                # Contact Summary Information
                o.write(summary % (result[0], process_phone(result[1]), result[2], result[3],
                                 result[4], result[5], result[6], result[7]))
                # Contact Detailed Information
                for interaction in answer_interactions:
                    display_name = interaction[0]
                    identifier = interaction[1]
                    time = interaction[6]
                    # Messages Received from Contact
                    if result[1] == identifier:
                        who = display_name
                        number = process_phone(identifier)
                        out = "%s: Message received from %s [%s]\n" % (time, who, number)
                        o.write(out)
                    #  Messages Sent to Contact
                    elif identifier is None and result[1] == interaction[7].split(';')[2]:
                        derived_num = interaction[7].split(';')[2]
                        for contact in contacts:
                            if contact == derived_num:
                                who = contacts[contact]
                        number = process_phone(derived_num)
                        out = "%s: Message sent to %s [%s]\n" % (time, who, number)
                        o.write(out)
                o.write("\n#=================================================================#\n")


if __name__ == '__main__':
    from helpers.mac_path_handler import process_directory_paths
    database, out_path = process_directory_paths()
    process_interactions(database, out_path)
else:
    from modules.helpers.mac_path_handler import process_directory_paths
