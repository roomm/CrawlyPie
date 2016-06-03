class NewSite():
    def __init__(self, sit, entity, fields, path):
        self.site = sit
        self.entty = entity
        self.fields = fields
        self.path = path

    def write_entity(self):
        with open(self.path+"/entities/" + self.site + ".py", "w") as fil:
            fil.write("class " + self.entty + ":\n")
            fil.write('    def __init__(self):\n')
            fil.write('        self.item_url = ""\n')
            fil.write('        self.site = ""\n')
            for field in self.fields:
                fil.write('        self.' + field + ' = ""\n')

    def write_yaml(self):
        with open(self.path+"/yaml/" + self.site + ".yaml", "w") as fil:
            fil.write("core:\n")
            fil.write("\tsite: \"http://www.example.com\"\n")
            fil.write("\tpaginationUrl: \"/page/{0}\"\n\n")

            fil.write("pagination:\n")
            fil.write("\titem: \n")
            fil.write("\t\txpath: ''\n")
            fil.write("\tmax_pages: \n")
            fil.write("\t\txpath: ''\n\n")

            fil.write("info:\n")
            for field in self.fields:
                fil.write("\t" + field + ": \n")
                fil.write("\t\txpath: ''\n")

    def write_site(self):
        with open(self.path+"/sites/" + self.site + ".py", "w") as fil:
            fil.write("from generic import GenericSite\n\n\n")
            fil.write("class " + self.site.title() + " (GenericSite):\n")
            fil.write("    def __init__(self):\n")
            fil.write('        GenericSite.__init__(self, "' + self.site + '", "' + self.entty + '", False)\n')
            fil.write("        self.set_config(\"" + self.site + ".yaml\")\n\n")
            fil.write("    def get_items(self, page_i, page_e):\n")
            fil.write("        pages_range = range(page_i, page_e + 1)\n")
            fil.write('        # Getting Items\n')
            fil.write('        self._go_get_pages(pages_range)\n')
            fil.write('        # Parsing Items\n')
            fil.write('        self._parse_items()\n')
            fil.write('        # Save Items\n')
            fil.write('        self._save_elements()\n\n')
            fil.write('    def _save_elements(self):\n')
            fil.write('        pass\n')
