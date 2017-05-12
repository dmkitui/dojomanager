# dojomanager
# dojo_manager.py

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/57db3d31e7774dafbf64944faefdcce8/badge.svg)](https://www.quantifiedcode.com/app/project/57db3d31e7774dafbf64944faefdcce8)

[![Coverage Status](https://coveralls.io/repos/github/kitui/dojomanager/badge.svg?branch=master)](https://coveralls.io/github/kitui/dojomanager?branch=master)

[![Build Status](https://travis-ci.org/kitui/dojomanager.svg?branch=master)](https://travis-ci.org/kitui/dojomanager)

## 1. dojo_manager.py

A commandline program to manage the automated management of the two types of rooms available at the Amity facility available for new staff and fellow

## 2. Installation

Clone/download this repo and run it via the commandline. Check the list of Requirements.txt for required packages

## 3. Usage

Usage: dojo_manager.py [command]

Commands:
```
    add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
    create_room Creates a room type of <room_type> called <room_name>
    add_person Adds a person, and assigns the person to a randomly chosen existing room
    add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
    reallocate_person <person_identifier> <new_room_name>
    print_room <room_name>
    print_allocations [<-o=filename>]
    print_unallocated [<-o=filename>]
    load_people (<people_file>)
    save_state [--db=sqlite_database]​
    load_state [--db=sqlite_database]​
    help
    clear
    exit
```
arguments: create_room Creates a room type of <room_type> called <room_name> add_person Adds a person, and assigns the person to a randomly chosen existing room

## 4. Contributing

Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request

## 5. History

Current: Version 0

## 6. Credits

The Andela fellowship cohort 17

## 7. License

This project is licensed under the MIT License

## 8. Author

@kitui