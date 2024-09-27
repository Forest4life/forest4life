#!/usr/bin/python3
"""
This module contains all the classes needed
for forest4life project.
"""

import json

class infos():
    """This class contains information about the organization."""
    storage = "info.json"
    partners = {}
    
    def __init__(self, location="Kigali-Rwanda", email="tubayeho@ac.rica.rw",
                 tel="+250781650592", twitter="https://x.com/Forest4lifec",
                 facebook="https://www.facebook.com/profile.php?id=100093036820473",
                 linkedin="https://www.linkedin.com/company/forest4life/about/",
                 instagram="instagram.com"):
        """Initialize the objects of this class."""
        self.socials = {}
        self.socials["facebook"] = facebook
        self.socials["twitter"] = twitter
        self.socials["instagram"] = instagram
        self.socials["linkedin"] = linkedin
        
        self.location = location
        self.contact = {}
        self.contact["email"] = email
        self.contact["tel"] = tel

    def to_dict(self):
        """return a dictionary of all attributes."""
        the_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                for key2, value2 in value.items():
                    the_dict[key2] = value2
            else:
                the_dict[key] = value
        return the_dict
    
            
        
    def save(self):
        """Save the object."""
        with open(self.__class__.storage, "w") as info:
            json.dump(self.to_dict(), info)
        

    def load(self):
        """load the dictionary."""
        with open(self.__class__.storage, "r") as info:
            dict = json.load(info)
        self.__init__(**dict)
