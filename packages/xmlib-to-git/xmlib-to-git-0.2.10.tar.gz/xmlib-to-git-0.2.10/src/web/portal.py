# -*- coding: utf-8 -*-

import os, base64, re
from .webpagedef import WebPageDef
from src.utils import my_tools


class Portal(object):
    """
    Défini un portail Rollase
    """

    def __init__(self, portal, app_dir):
        self.id = portal["id"]
        self.orig_id = portal["origId"]
        self.is_main = portal["isMain"]
        self.name = portal.SiteName.cdata
        self.stylesheet = portal.Stylesheet.cdata
        self.header = base64.b64decode(portal.Header.cdata)
        self.footer = base64.b64decode(portal.Footer.cdata)
        if hasattr(portal.WebPageDefs, "WebPageDef"):
            self.webpages = portal.WebPageDefs.WebPageDef
        else:
            self.webpages = ""
        dirname = my_tools.mysplit(self.name, 50)
        self.portal_dir = "{}/portals/{}".format(app_dir, dirname)
        self.properties = portal.__dict__

    def to_file(self):
        # fichier de propriétés
        if not os.path.exists(self.portal_dir):
            os.makedirs(self.portal_dir)
        file = open("{}/PROPERTIES.md".format(self.portal_dir), 'w+')
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- isMain : {}\n".format(self.is_main))

            # Propriétés
            file.write("\n\n## Properties\n")
            for el in self.properties["children"]:
                file.write("- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"]))

        header = open("{}/header.html".format(self.portal_dir), 'w+')
        with header:
            header.write(self.header.decode("utf-8"))

        footer = open("{}/footer.html".format(self.portal_dir), 'w+')
        with footer:
            footer.write(self.footer.decode("utf-8"))

        if self.webpages:
            self.create_web_pages()

    def create_web_pages(self):
        # objets de l'application
        for webpage in self.webpages:
            new_webpagedef = WebPageDef(webpage, self.portal_dir)
            new_webpagedef.to_file()
