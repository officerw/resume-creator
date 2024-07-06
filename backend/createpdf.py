from pdflatex import PDFLaTeX
import os
import time
import math
import json
import subprocess
import re

# We create a Resume object that consists of a name,
# list of contact info, and a list of sections.
#
# In the json argument, we expect a json object with the
# following structure:
# {
#     "name": "",
#     "contact_info": ["", "", ""],
#     "sections": Section[]
# }
class Resume:
    def __init__(self, json):
        self.name = handleSpecialChars(json["name"])

        contact_info = []
        for item in json["contact_info"]:
            contact_info.append(handleSpecialChars(item))

        self.contact_info = contact_info

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
#     "is_experiences": true,
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
#     "is_experiences": true,
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
        self.section_name = handleSpecialChars(json["section_name"])
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
        self.list_title = handleSpecialChars(json["list_title"])
        self.list_content = handleSpecialChars(json["list_content"])

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
        self.experience_title = handleSpecialChars(json["experience_title"])
        self.location = handleSpecialChars(json["location"])
        self.organization = handleSpecialChars(json["organization"])
        self.tenure = handleSpecialChars(json["tenure"])

        content = []
        for item in json["content"]:
            content.append(handleSpecialChars(item))

        self.content = content

def compile(resumeInfo):
    # Load JSON information into Resume object to be parsed
    json_obj = json.loads(json.dumps(resumeInfo))
    template = json_obj["template"]
    data = Resume(json_obj["resume_info"])

    sections_info = ""
    if template == "template5":
        sections_info = addSectionInfoTabularly(data, template)
    else:
        sections_info = addSectionInfo(data, template)

    # Read the LaTeX template
    file = open(f"./tex_templates/{template}.tex", "r")
    filestr = file.read()

    # Replace name and address placeholders
    filestr = filestr.replace("NAME", data.name)

    num_contact_info = len(data.contact_info)
    if template == "template1" or template == "template3":
        # Select contact info separator based on template
        contact_info_separator = " $\\bullet$ "
        if template == "template3":
            contact_info_separator = " $\\vert$ "

        # If there are more than 3 pieces of contact information, split the
        # contact information into two lists
        if num_contact_info > 3:
            contact_info_1 = data.contact_info[:num_contact_info//2]
            contact_info_2 = data.contact_info[num_contact_info//2:]

            # Add bullet points between contact information values
            contact_info_1 = contact_info_separator.join(contact_info_1)
            contact_info_2 = contact_info_separator.join(contact_info_2)

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info_1)
            filestr = filestr.replace("CONTACT_INFO_2", contact_info_2)
        else:
            # Add bullet points betwen contact information
            contact_info = " $\\bullet$ ".join(data.contact_info)

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO_1", contact_info)
            filestr = filestr.replace("CONTACT_INFO_2", "")
    elif template == "template2" or template == "template5":
        if num_contact_info > 4:
            contact_info_1 = data.contact_info[:math.ceil(num_contact_info/2)]
            contact_info_2 = data.contact_info[math.ceil(num_contact_info/2):]

            # Make two rows of info, evenly spaced information
            contact_info_1 = " & ".join(contact_info_1)
            contact_info_2 = " & ".join(contact_info_2)

            # Make tables to fit data, variable number of elements per row
            contact_info_str = "\\begin{center}\n\\begin{tabular}{ "

            for x in contact_info_1:
                contact_info_str = contact_info_str + "c "

            contact_info_str = contact_info_str + "}\n" + contact_info_1 + "\\end{tabular}\\end{center}\n\n"

            contact_info_str = contact_info_str + "\\begin{center}\n\\begin{tabular}{ "

            for x in contact_info_2:
                contact_info_str = contact_info_str + "c "

            contact_info_str = contact_info_str + "}\n" + contact_info_2 + "\\end{tabular}\\end{center}"

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO", contact_info_str)
        else:
            # Evenly space info
            contact_info = " & ".join(data.contact_info)

            # Make tables to fit data, variable number of elements per row
            contact_info_str = "\\begin{center}\n\\begin{tabular}{ "

            for x in data.contact_info:
                contact_info_str = contact_info_str + "c "

            contact_info_str = contact_info_str + "}\n" + contact_info + "\\end{tabular}\\end{center}\n\n"

            # Insert into template
            filestr = filestr.replace("CONTACT_INFO", contact_info_str)
    elif template == "template4":
        # Add contact info into a table
        contact_info_str = ""
        # All all contact items except for first one
        for contact_item in data.contact_info[:-1]:
            contact_info_str = contact_info_str + "& " + contact_item + " \\\\\n"

        contact_info_str = contact_info_str + "& " + data.contact_info[len(data.contact_info) - 1]

        # Insert into template
        filestr = filestr.replace("CONTACT_INFO", contact_info_str)

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

    if result.stderr != "":
        print("Error generating PDF from temporary .tex file")
        print(result.stderr)
        return

    # Delete temporary .tex file, .log, and .aux files from PDF creation
    deleteFile(tempTexFilePath, fileCreationTime + ".aux", fileCreationTime + ".log")

    return fileCreationTime + ".pdf"

# Delete file based on name
def deleteFile(*files):
    for file in files:
        os.remove(file)

# Add section info normally
def addSectionInfo(jsonData, template):
    sections_info = ""
    for section in jsonData.sections:
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

                bullet_point = ""
                if template == "template4":
                    bullet_point = "[$\\blacklozenge$]"

                # Add experience descriptions
                for item in experience.content:
                    sections_info += "\\item" + bullet_point + " " + item + "\n"

                # End list
                sections_info += "\\end{itemize}\n\n"
        else:
            for list in section.content:
                # Add list title and list content
                sections_info += "\\listsection{" + list.list_title + "}{" + list.list_content + "}\n\n"

    return sections_info

# Add section info tabularly
def addSectionInfoTabularly(jsonData, template):
    sections_info = ""
    for section in jsonData.sections:
        # For each section, add a table
        sections_info += "\\begin{tabular}{ m{1.2in} | m{5.9in} }\n"
        sections_info += "\\textbf{" + section.section_name + "} "

        # If the section contains experiences, parse the experience info
        if section.is_experiences:
            for experience in section.content:
                # Add experience header into table
                sections_info += "& \\experienceheader{" + experience.experience_title + "}{" + experience.location + "}{" + experience.organization + "}{" + experience.tenure + "} \\\\\n"

                # Add a list for the experience descriptions
                sections_info += "& \\begin{itemize}\n"
                sections_info += "\\setlength\\itemsep{0pt}\n"

                bullet_point = ""
                
                # Add experience descriptions
                for item in experience.content:
                    sections_info += "\\item" + bullet_point + " " + item + "\n"

                # End list
                sections_info += "\\end{itemize}\\\\\n"
        else:
            for list in section.content:
                # Add list title and list content
                sections_info += "& \\listsection{" + list.list_title + "}{" + list.list_content + "}\\\\\n"

        # End section and table
        sections_info += "& \\\\\n"
        sections_info += "\\end{tabular}\n\n"

    return sections_info

# Remove/update special characters for safety/formatting
def handleSpecialChars(inputStr):
    # Remove the following special chars
    rmv_special_chars = r"[~|\\{}<>^]"
    # Fix the following special chars to make them usable
    fix_special_chars = "$#%&€£"

    inputStr = re.sub(rmv_special_chars, "", inputStr)

    for char in fix_special_chars:
        inputStr = inputStr.replace(char, "\\" + char)

    return inputStr