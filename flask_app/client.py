import requests
import re

class Package(object):
    def __init__(self, name, description, link):
        
        self.name = name
        self.description = description
        self.link = link 

    def __repr__(self):
        return self.name + "\n" + self.description  + "\n" + self.link


class PackageClient(object):
    def __init__(self):
        self.sess = requests.Session()

        URL = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
        page = requests.get(URL)
        all_packages_html = page.text.split("<tr>")[1:]

        self.all_package_names = [re.search("index.html\">(.*)</a></td><td>", row).group(1) for row in all_packages_html]

        all_packages_html_no_newline = [row.replace('\n',' ') for row in all_packages_html]
        self.all_package_descriptions = [re.search("</td><td>(.*)</td></tr>", row).group(1) for row in all_packages_html_no_newline]

        website_beginning = "https://cran.r-project.org/web/packages/"
        website_end = "/index.html"
        self.all_package_links = [website_beginning + re.search("web/packages/(.*)/index.html", row).group(1) + website_end for row in all_packages_html]



    def search(self, search_string):
        """
        See if a package matches the search query
        """

        try: 
            index_of_package = self.all_package_names.index(search_string)

            name = self.all_package_names[index_of_package]
            description = self.all_package_descriptions[index_of_package]
            link = self.all_package_links[index_of_package]

            result = [Package(name, description, link)]
        
        except ValueError:
            raise ValueError(f'Could not find any packages using \'{search_string}\'')

        return result

    def retrieve_package_by_name(self, package_name):

        try: 
            index_of_package = self.all_package_names.index(package_name)

            name = self.all_package_names[index_of_package]
            description = self.all_package_descriptions[index_of_package]
            link = self.all_package_links[index_of_package]

            package = Package(name, description, link)
        
        except ValueError:
            raise ValueError(f'Could not find any packages using \'{package_name}\'')

        return package


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = PackageClient()

    packages = client.search("ggplot2")

    for p in packages:
        print(p)

