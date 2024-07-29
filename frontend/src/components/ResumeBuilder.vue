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
    
    const API_ENDPOINT = "https://resume-creator-cffw6ike3q-uc.a.run.app/api/compilepdf"

    interface Contact {
        id: number
        info: String
    }

    type List = {
        list_title: string
        list_content: string
    }

    type Section = {
        id: number
        section_name: string
        section_type: string
        content: Array<List|Experience>
    }

    type Experience = {
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    // Send PDF URL to PDF Viewer to display and allow download
    const emit = defineEmits(["sendPdfUrl"])

    // Accept new selected template
    const props = defineProps({
        template: {
            type: String,
            required: true
        }
    })

    // Store list of sections
    const sections: (Section)[] = []

    // Store resume information
    const resumeInfo = ref({
        name: "",
        contact_info: [""],
        sections: sections
    })

    // Store set resume information, set by imported JSON
    const setResumeInfo = ref({
        name: "",
        contact_info: [""],
        sections: sections
    })
    
    // Update contacts based on provided information
    function updateContacts(contacts: Contact[]) {
        let list = []
        for (let i = 0; i < contacts.length; i++) {
            list.push(contacts[i].info.valueOf())
        }

        resumeInfo.value.contact_info = list
    }

    // Compile the resume information into a PDF
    async function compilePDF() {
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
            console.log(result)
            if (result != undefined) {
                setResumeInfo.value = JSON.parse(result)
            }
        }
        
        // Verify user uploaded .json file or is using sample resume
        var file = null
        if (usingSampleResume) {
            setResumeInfo.value = SampleResume
            // Wait for system to process JSON
            await new Promise(r => setTimeout(r, 1000));
            compilePDF()
        } else if (upload != null && upload.files != null && upload.files[0] != undefined && upload.files[0].name.includes(".json")) {
            file = upload.files[0]
            reader.readAsText(file)
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
        <NameContactInfo 
            @update-name="(name) => (resumeInfo.name = name)" 
            @update-contacts="(contacts) => updateContacts(contacts)"
            :set-name="setResumeInfo.name"
            :set-contacts="setResumeInfo.contact_info"/>

        <ResumeSections
            @update-sections="(sections) => (resumeInfo.sections = sections)"
            :set-sections="setResumeInfo.sections"/>
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
