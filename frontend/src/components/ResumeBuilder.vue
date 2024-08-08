<!--
  ResumeBuilder

  This contains fields for the user to populate with information that would be
  contained in their resume. This information is compiled into a Javascript
  object and is sent to the TemplateEditor for processing.
-->

<script setup lang="ts">
    import NameContactInfo from "../components/NameContactInfo.vue"
    import ResumeSections from "../components/ResumeSections.vue"
    import SampleResume from "../../public/static/sample_resume.json"
    import { onMounted, ref, watch } from "vue"
    
    const API_ENDPOINT = "/api/compilepdf"
    //const API_ENDPOINT = "https://resume-creator-cffw6ike3q-uc.a.run.app/api/compilepdf"

    type NameContactInfo = {
        name: string
        contact_info: Array<ContactInfo>
    }

    type ContactInfo = {
        id: number
        info: string
    }

    type List = {
        id: number
        list_title: string
        list_content: string
    }

    type Section = {
        id: number
        section_name: string
        section_type: string
        list_content: Array<List>
        exp_content: Array<Experience>
    }

    type Experience = {
        id: number
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    type ResumeInfo = {
        nameContactInfo: NameContactInfo
        sections: Array<Section>
    }

    // Send PDF URL to PDF Viewer to display and allow download
    const emit = defineEmits(["sendPdfUrl"])

    // Accept info on the template selected
    const props = defineProps({
        template: {
            type: String,
            required: true
        }
    })

    // Store resume info
    const resumeInfo = ref({
        nameContactInfo: {
            name: "",
            contact_info: [{ id: 1, info: ""}]
        },
        sections: new Array<Section>()
    })

    // Compile the resume information into a PDF
    async function compilePDF() {
        console.log("Test")
        console.log(JSON.stringify({ template: props.template, resume_info: resumeInfo.value}))
        // POST request to backend with resume info as JSON
        const response = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ template: props.template, resume_info: resumeInfo.value})
        })
        // Get generated pdf as blob response
        const compiledPDF = await response.blob();
        const pdfURL = URL.createObjectURL(compiledPDF)

        emit("sendPdfUrl", pdfURL)
    }

    // Save resume info as JSON so users can save progress
    function saveJSON() {
        var jsonText = JSON.stringify(resumeInfo.value)
        var fileName = "resume-info.json"
        // Create a download element internally to allow download
        var download = document.createElement("a")
        download.setAttribute("href", "data:application/json;charset=utf-8," + encodeURIComponent(jsonText))
        download.setAttribute("download", fileName)
        // Make download tag invisible on document
        download.style.display = "none"
        document.body.appendChild(download)
        // Have user click on download tag and remove tag
        download.click()
        document.body.removeChild(download)
    }

    // Upload resume info as JSON so users can update info
    async function readJSON(usingSampleResume: boolean) {
        var upload = (<HTMLInputElement>document.getElementById("json-upload"))

        // Functionality after reading file
        var reader = new FileReader()
        reader.onload = () => {
            // If the information read is a string, parse as JSON
            var result = reader.result?.toString()
            if (result != undefined) {
                return JSON.parse(result)
            }
        }
        
        // Verify user uploaded .json file or is using sample resume
        var file = null
        var uploadedResumeInfo
        if (usingSampleResume) {
            uploadedResumeInfo = JSON.parse(JSON.stringify(SampleResume))
            console.log(SampleResume)
        } else if (upload != null && upload.files != null && upload.files[0] != undefined && upload.files[0].name.includes(".json")) {
            file = upload.files[0]
            uploadedResumeInfo = reader.readAsText(file)
        }

        // Use uploaded resume info to modify internal resume info
        if (uploadedResumeInfo) {
            setResumeBasedOnJSON(uploadedResumeInfo)
        }
            
    }

    // Use uploaded resume info to modify internal resume info
    function setResumeBasedOnJSON(uploadedResumeInfo: ResumeInfo) {
        console.log(uploadedResumeInfo)

        // Set name based on uploaded info
        resumeInfo.value.nameContactInfo.name = uploadedResumeInfo.nameContactInfo.name

        // Delete previous contact info and replace with new info
        var contactInfo = resumeInfo.value.nameContactInfo.contact_info
        var uploadedContactInfo = uploadedResumeInfo.nameContactInfo.contact_info
        while (contactInfo.length > 1)
            contactInfo.pop()
        // Set new info
        contactInfo[0].info = uploadedContactInfo[0].info
        for (let i = 1; i < uploadedContactInfo.length; i++) {
            contactInfo.push({ id: i + 1, info: uploadedContactInfo[i].info })
        }
        
        // Delete previous sections and replace with new info
        var sections = resumeInfo.value.sections
        var uploadedSections = uploadedResumeInfo.sections
        while (sections.length > 0)
            sections.pop()

        // Set new sections
        for (let i = 0; i < uploadedSections.length; i++) {
            sections.push({ id: i + 1, section_name: uploadedSections[i].section_name,
                section_type: uploadedSections[i].section_type,
                list_content: uploadedSections[i].list_content,
                exp_content: uploadedSections[i].exp_content
            })

            console.log(sections)
        }
    }

    // On mount, link import button to file input
    onMounted(() => {
        const fileInputButton = document.getElementById("import-resume-json")
        const fileInput = document.getElementById("json-upload")

        fileInputButton?.addEventListener("click", () => {
            fileInput?.click()
        })
    })

    // When user selects new template, compile
    watch(() => props.template, () => {
        compilePDF()
    })

</script>

<template>
    <!-- UI to save resume info as JSON, import JSON, and compile into PDF -->
    <div class="compile-resume-info">
        <div class="save-json">
            <button id="save-resume-json" @click="saveJSON()"><img src="/static/download.png">Download Progress</button>
        </div>

        <div class="read-json">
            <button id="import-resume-json"><img src="/static/upload.png">Upload Progress</button>
            <input type="file" id="json-upload" accept=".json" @change="readJSON(false)" style="display:none;"/>
        </div>
    </div>

    <div class="compile-resume-info">
        <div class="sample-resume">
            <button id="sample-resume-button" @click="readJSON(true)">Try Sample Resume</button>
        </div>

        <div class="compile-resume">
            <button id="compile-resume-button" @click="compilePDF()">Convert into PDF</button>
        </div>
    </div>

    <!-- Warn the user that certain characters may not be used -->
    <div id="special-chars-warning">
        <h5>The following special characters cannot be used: ~, |, \, {, }, <, >, ^</h5>
    </div>

    <!-- Allow user to build resume name, contact info, and resume sections -->
    <div class="resume-builder">
        <NameContactInfo v-model="resumeInfo.nameContactInfo"/>

        <ResumeSections v-model="resumeInfo.sections"/>
    </div>
    
</template>

<style>
    .resume-builder {
        width: 100%;
        height: fit-content;
    }

    .compile-resume-info {
        display: flex;
        margin: 10px 0;
    }

    .save-json {
        width: 50%;
    }

    .read-json {
        width: 50%;
    }

    .sample-resume {
        width: 50%;
    }

    .compile-resume {
        width: 50%;
    }

    .read-json button {
        background-color: #3491ff;
        border-radius: 7px;
        height: 2rem;
        width: 80%;
        display: flex;
        color: #000000;
        border: none;
        align-items: center;
        justify-content: space-evenly;
        margin: 0 2rem;
    }

    .compile-resume-info button  {
        background-color: #3491ff;
        border-radius: 7px;
        height: 2rem;
        width: 80%;
        color: #000000;
        display: flex;
        border: none;
        align-items: center;
        justify-content: space-evenly;
        margin: 0 2rem;
    }

    .import-sample button  {
        background-color: #3491ff;
        border-radius: 7px;
        height: 2rem;
        width: 80%;
        display: flex;
        color: #000000;
        border: none;
        align-items: center;
        justify-content: space-evenly;
        margin: 0 2rem;
    }

    #special-chars-warning {
        bottom: 0;
    }

</style>
