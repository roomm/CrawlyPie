import sys


def new_site(path):
    name = raw_input("Site Name: ")
    entty = raw_input("Entity Name: ")
    fields = []

    while True:
        field = raw_input("Field Name: ")
        if field == "":
            break
        fields.append(field)

    from functions.new_site import NewSite
    newsitter = NewSite(name, entty, fields, path)
    newsitter.write_entity()
    newsitter.write_yaml()
    newsitter.write_site()


def print_menu():
    print "CRAWLYPIE"
    print "NEW:"
    print "\tnew:site"


if __name__ == "__main__":
    import os

    path = os.getcwd()
    if len(sys.argv) == 1:
        print_menu()
    elif len(sys.argv) == 2:
        try:

            if sys.argv[1] == "new:site":
                new_site(path)
            else:
                print "ERROR-Command not found"

        except KeyboardInterrupt:
            print "\n***CANCELLED***"
            exit(0)
