<!--
  ResumeBuilder

  This contains fields for the user to populate with information that would be
  contained in their resume. This information is compiled into a Javascript
  object and is sent to the TemplateEditor for processing.
-->

<script setup lang="ts">
    import NameContactInfo from "../components/NameContactInfo.vue"
    import ResumeSections from "../components/ResumeSections.vue"
    import { ref, watch } from "vue"
    

    type List = {
        list_title: string
        list_content: string
    }

    type Experience = {
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    type Section = {
        id: number
        name: string
        type: string
        content: (List|Experience)[]
    }

    // Store list of sections
    const sections: (Section)[] = []

    // Store resume information
    const resumeInfo = ref({
        name: "",
        contact_info: [""],
        sections: sections
    })

    interface Contact {
        id: Number
        info: String
    }
    
    // Update contacts based on provided information
    function updateContacts(contacts: Contact[]) {
        let list = []
        for (let i = 0; i < contacts.length; i++) {
            list.push(contacts[i].info.valueOf())
        }

        resumeInfo.value.contact_info = list
    }

    // Compile the resume information into a PDF
    function compilePDF() {
        console.log(resumeInfo.value)
    }

    watch(resumeInfo.value, (newResume) => {
        console.log(newResume)
    })

</script>

<template>
    <div class="compile-resume-info">
        <button id="compile-resume-button" @click="compilePDF()">Compile into PDF</button>
    </div>

    <div class="resume-builder">
        <NameContactInfo 
            @update-name="(name) => (resumeInfo.name = name)" 
            @update-contacts="(contacts) => updateContacts(contacts)"/>

        <ResumeSections
            @update-sections="(sections) => resumeInfo.sections = sections"/>
    </div>
</template>

<style>
    .resume-builder {
        width: 100%;
        height: fit-content;
    }
</style>
