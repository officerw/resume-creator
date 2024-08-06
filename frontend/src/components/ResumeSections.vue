
<script setup lang="ts">
    import { ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Section from "./Section.vue"

    type List = {
        id: number
        list_title: string
        list_content: string
    }

    type Experience = {
        id: number
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    type Section = {
        id: number
        section_name: string
        section_type: string
        list_content: Array<List>
        exp_content: Array<Experience>
    }

    const sections = defineModel<Array<Section>>({
        required: true
    })

    // Add a section based on the type
    function addSection(sectionType: string) {
        // Get index of section
        let index = 1
        // If there is at least one section, get the maximum index value
        if (sections.value.length > 0) {
            for (let i = 0; i < sections.value.length; i++) {
                var currSection = sections.value[i]

                if (currSection.id >= index) {
                    index = currSection.id + 1
                }
            }
        }

        // Add section based on type
        if (sectionType == "list") {
            sections.value.push({ id: index, section_name: "", section_type: sectionType, list_content: [{ id: 1, list_title: "", list_content: "" }], exp_content: []})
        } else {
            sections.value.push({ id: index, section_name: "", section_type: sectionType, list_content: [], exp_content: [{ id: 1, experience_title: "", location: "", organization: "", tenure: "", content: [""] }] })
        }
    }

    // Remove a section when the user deletes it
    function removeSection(idToRemove: Number) {
        let updatedSections: (Section)[] = []
        for (let i = 0; i < sections.value.length; i++) {
            let currentSection = sections.value[i]
            if (currentSection.id != idToRemove) {
                updatedSections.push(currentSection)
            }
        }

        sections.value = updatedSections
    }

</script>

<template>
    <div class="resume-sections">
        <h4 id="sections-title">Sections</h4>

        <!-- List of sections -->
        <div v-if="sections.length > 0" class="sections-list">
            <div v-for="(section, i) in sections">
                <Section v-model="sections[i]" 
                @delete-section="(idToRemove) => removeSection(idToRemove)" ></Section>
            </div>
            <!--<draggable v-model="sections" item-key="id">
                <template #item="{element}">
                    <Section v-model="element"
                        @delete-section="(idToRemove) => removeSection(idToRemove)"></Section>
                </template>
            </draggable>-->
        </div>

        <!-- The following section allows the user to add different kinds of sections to the resume builder -->
        <div class="section-list-buttons">
            <button id="add-experience" @click="addSection('experience')">Add Experience Section</button>
            <button id="add-list" @click="addSection('list')">Add List Section</button>
        </div>
    </div>
</template>

<style>

    #sections-title {
        margin: 4px 0;
        font-weight: bold;
        text-align: center;
    }

    .sections-list {
        padding: 5px;
        background-color: lightgray;
        border-radius: 10px 10px 0 0;
    }

    .section-list-buttons {
        display: flex;
        background-color: lightgray;
    }

    button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }
</style>
