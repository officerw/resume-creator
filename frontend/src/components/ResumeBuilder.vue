<!--
  ResumeBuilder

  This contains fields for the user to populate with information that would be
  contained in their resume. This information is compiled into a Javascript
  object and is sent to the TemplateEditor for processing.
-->

<script setup lang="ts">
    import NameContactInfo from "../components/NameContactInfo.vue"
    import ResumeSections from "../components/ResumeSections.vue"
    import { ref } from "vue"

    // Store resume information
    const resumeInfo = ref({
        name: "",
        contact_info: [""],
        sections: []
    })

    // Define interface for contact information
    // Refer to NameContactInfo.vue for structure of
    // Contact object
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

    // Update name
    function updateName(name: string) {
        resumeInfo.value.name = name
    }

</script>

<template>
    <div class="resume-builder">
        <NameContactInfo 
            @update-name="(name) => updateName(name)" 
            @update-contacts="(contacts) => updateContacts(contacts)"
            />

        <ResumeSections/>
    </div>
</template>

<style>
    .resume-builder {
        width: 100%;
        height: fit-content;
    }
</style>
