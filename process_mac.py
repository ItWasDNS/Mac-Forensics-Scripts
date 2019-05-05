"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7 on macOS
    Description: Parse Mac Artifacts
"""

import os
import sys
from modules.mac_interactions_ical import process_ical
from modules.mac_interactions_imessage import process_interactions
from modules.mac_knowledge_entities import process_entities
from modules.mac_knowledge_spotlight_events import process_spotlight

warn_1 = "Directory does not exist. Please enter a valid directory to process."
warn_2 = "Directory already exists. Continuing could overwrite existing data."

if __name__ == '__main__':
    try:
        # Prepare root directory to process
        while True:
            root = input("Enter root directory of APFS Filesystem to Process: ")
            if os.path.exists(root):
                break
            else:
                print(warn_1)

        # Prepare output directory
        while True:
            out = input("Enter full path to output results: ")
            if os.path.exists(out):
                print(warn_2)
                advance = input("Do you wish to continue (y/n): ")
                if advance.strip().lower() == 'y':
                    break
            else:
                os.mkdir(out)
                break
    except KeyboardInterrupt:
        sys.exit(1)

    # Locations to parse
    system_interactionC = os.path.join(root, '/private/var/db/CoreDuet/People/interactionC.db')
    system_knowledgeC = os.path.join(root, '/private/var/db/CoreDuet/Knowledge/knowledgeC.db')
    user_knowledgeC = []
    user_knowledgeC_loc = 'Library/Application Support/Knowledge/knowledgeC.db'
    for user_subdir in next(os.walk('/Users'))[1]:
        if user_subdir != 'Guest' and user_subdir != 'Shared':
            db_path = os.path.join(root, '/Users', user_subdir, user_knowledgeC_loc)
            user_knowledgeC.append(db_path)

    # Process artifacts
    print("Processing: '/private/var/db/CoreDuet/People/interactionC.db'")
    process_ical(db=system_interactionC, output_path=out)
    process_interactions(db=system_interactionC, output_path=out)
    print("Processing: '/private/var/db/CoreDuet/Knowledge/knowledgeC.db'")
    process_spotlight(db=system_knowledgeC, output_path=out)
    print("Processing: User Specific 'knowledgeC.db'")
    for entry in user_knowledgeC:
        print("    %s" % entry)
        process_entities(db=entry, output_path=out)

    # Processing Complete
    print("Processing Completed")
