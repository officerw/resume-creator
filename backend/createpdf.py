from pdflatex import PDFLaTeX
import tempfile
import json

# We create a Resume object that consists of a name,
# list of contact info, and a list of sections.
#
# In the json argument, we expect a json object with the
# following structure:
# {
#     "name": "",
#     "address": "",
#     "contact-info": ["", "", ""],
#     "sections": Section[]
# }
class Resume:
    def __init__(self, json):
        self.name = json["name"]
        self.address = json["address"]
        self.contact_info = json["contact-info"]

        # Get a list of sections associated with this resume
        sections = json["sections"]
        self.sections = []
        for section in sections:
            self.sections.append(Section(section))

# We create a Section object that has a name
# type (either lists or experiences), and content.
# The content consists of either List's or Experience's
#
# In the json argument, we expect a json object with the
# following structure:
# {
#     "section-name": "",
#     "section-type": "lists",
#     "content": [
#         {
#             "list-title": "",
#             "list-content": ""
#         }
#     ]
# }
# or the following structure
# {
#     "section-name": "",
#     "section-type": "experiences",
#     "content": [
#         {
#             "experience-title": "",
#             "location": "",
#             "organization": "",
#             "tenure": "",
#             "content": ["", "", ""]
#         }
#     ]
# }
class Section:
    def __init__(self, json):
        self.section_name = json["section-name"]
        self.is_experiences = json["section-type"] == "experiences"
    
        # Get the experience or list content associated with this section
        self.content = []
        if self.is_experiences:
            for experience in json["content"]:
                self.content.append(Experience(experience))
        else:
            for list in json["content"]:
                self.content.append(List(list))

# We create a List object that has a list
# title and list of values associated with it
#
# In the json argument, we expect a json object with
# the following structure
# {
#    "list-title": "",
#    "list-content": ""
# }
class List:
    def __init__(self, json):
        self.list_title = json["list-title"]
        self.list_content = json["list-content"]

# We create an Experience object that
# organizes experience title, location, tenure,
# organization, and experience descriptions.
#
# In the json argument, we expect a json object with
# the following structure
# {
#   "experience-title": "",
#   "location": "",
#   "organization": "",
#   "tenure": "",
#   "content": ["", "", ""]
# }
class Experience:
    def __init__(self, json):
        self.experience_title = json["experience-title"]
        self.location = json["location"]
        self.organization = json["organization"]
        self.tenure = json["tenure"]
        self.content = json["content"]

def main():
    file = open("resume-info.json")

    data = Resume(json.load(file))

    sections_info = ""
    for section in data.sections:
        # For each section, add a section header
        sections_info += "\\sectionheader{" + section.section_name + "}\n\n"

        if section.is_experiences:
            for experience in section.content:
                # Add experience header
                sections_info += "\\experienceheader{" + experience.experience_title + "}{" + experience.location + "}{" + experience.organization + "}{" + experience.tenure + "}\n\n"

                # Add a list for the experience descriptions
                sections_info += "\\begin{itemize}\n"
                sections_info += "\\setlength\\itemsep{0pt}\n"

                # Add experience descriptions
                for item in experience.content:
                    sections_info += "\\item " + item + "\n"

                # End list
                sections_info += "\\end{itemize}\n\n"
        else:
            for list in section.content:
                # Add list title and list content
                sections_info += "\\skills{" + list.list_title + "}{" + list.list_content + "}\n\n"

    # Read the LaTeX template
    file = open("./tex_templates/template1.tex", "r")
    filestr = file.read()

    # Replace name and address placeholders
    filestr = filestr.replace("NAME", data.name)
    filestr = filestr.replace("ADDRESS", data.address)
    
    # Add bullet points between contact information values
    contact_info = " $\\bullet$ ".join(data.contact_info)
    
    # Replace contact information placeholder with contact information
    filestr = filestr.replace("CONTACT_INFO", contact_info)
    # Replace sections with actual sections specified by the user
    filestr = filestr.replace("SECTIONS", sections_info)  

    # Create a temporary .tex file to add .tex string
    print(filestr)

    #pdfl = PDFLaTeX.from_binarystring(filestr, "my_file")
    #pdf, log, cp = pdfl.create_pdf()



if __name__ == "__main__":
    main()