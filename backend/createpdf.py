from pdflatex import PDFLaTeX
import os
import time
import json
import subprocess

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
        self.contact_info = json["contact_info"]

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
        self.section_name = json["section_name"]
        self.is_experiences = json["section_type"] == "experience"
    
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
        self.list_title = json["list_title"]
        self.list_content = json["list_content"]

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
        self.experience_title = json["experience_title"]
        self.location = json["location"]
        self.organization = json["organization"]
        self.tenure = json["tenure"]
        self.content = json["content"]

def compile(resumeInfo):
    # Load JSON information into Resume object to be parsed
    json_obj = json.loads(json.dumps(resumeInfo))
    template = json_obj["template"]
    data = Resume(json_obj["resume_info"])
    
    sections_info = ""
    for section in data.sections:
        # For each section, add a section header
        sections_info += "\\sectionheader{" + section.section_name + "}\n\n"

        # If the section contains experiences, parse the experience information
        # Otherwise, parse the list information
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
                sections_info += "\\listsection{" + list.list_title + "}{" + list.list_content + "}\n\n"

    # Read the LaTeX template
    file = open(f"./tex_templates/{template}.tex", "r")
    filestr = file.read()

    # Replace name and address placeholders
    filestr = filestr.replace("NAME", data.name)

    num_contact_info = len(data.contact_info)
    print(template)
    if template == "template1":
        # If there are more than 3 pieces of contact information, split the
        # contact information into two lists
        if num_contact_info > 3:
            contact_info_1 = data.contact_info[:num_contact_info//2]
            contact_info_2 = data.contact_info[num_contact_info//2:]

            # Add bullet points between contact information values
            contact_info_1 = " $\\bullet$ ".join(contact_info_1)
            contact_info_2 = " $\\bullet$ ".join(contact_info_2)

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info_1)
            filestr = filestr.replace("CONTACT_INFO_2", contact_info_2)
        else:
            # Add bullet points betwen contact information
            contact_info = " $\\bullet$ ".join(data.contact_info)

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info)
            filestr = filestr.replace("CONTACT_INFO_2", "")
    elif template == "template2":
        print("hello")
        if num_contact_info > 4:
            contact_info_1 = data.contact_info[:num_contact_info//2]
            contact_info_2 = data.contact_info[num_contact_info//2:]

            # Make two rows of info, evenly spaced information
            contact_info_1 = "\\hfill " + " \\hfill ".join(contact_info_1) + " \\hfill"
            contact_info_2 = "\\hfill " + " \\hfill ".join(contact_info_2) + " \\hfill"

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info_1)
            filestr = filestr.replace("CONTACT_INFO_2", contact_info_2)
        else:
            # Evenly space info
            contact_info = "\\hfill " + " \\hfill ".join(data.contact_info) + " \\hfill"

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info)
            filestr = filestr.replace("\n\n\\vspace{5pt}\n\nCONTACT_INFO_2", "")

    # Replace sections with actual sections specified by the user
    filestr = filestr.replace("SECTIONS", sections_info)  

    # Create a temporary .tex file to add .tex string with a name determined
    # by the time of creation. Write to this file.
    fileCreationTime = str(time.time_ns())
    tempTexFilePath = "./" + fileCreationTime + ".tex"
    tempTexFile = open(tempTexFilePath, "a")
    tempTexFile.write(filestr)
    tempTexFile.close()

    # Create PDF based on .tex file
    result = subprocess.run(["pdflatex", tempTexFilePath], capture_output = True, text = True)

    print(result.stdout)
    print(result.returncode)

    if result.stderr != "":
        print("Error generating PDF from temporary .tex file")
        print(result.stderr)
        return

    # Delete temporary .tex file, .log, and .aux files from PDF creation
    #deleteFile(tempTexFilePath, fileCreationTime + ".aux", fileCreationTime + ".log")

    return fileCreationTime + ".pdf"

# Delete file based on name
def deleteFile(*files):
    for file in files:
        os.remove(file)
