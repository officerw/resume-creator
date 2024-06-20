
<script setup lang="ts">
    import { ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Section from "./Section.vue"

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
        section_name: string
        section_type: string
        content: Array<List|Experience>
    }

    // Update section info based on user input
    const emit = defineEmits(["updateSections"])
    // Update section info based on JSON imports
    const props = defineProps({
        setSections: {
            type: Array<Section>,
            required: true
        }
    })

    // Define index and reactive list of section information
    var index = 0
    const val: Section[] = []
    const sections = ref(val)
    // Define list of values set by JSON
    const setVal: Section[] = []
    const setSections = ref(setVal)

    // Add a section based on the type
    function addSection(sectionType: string) {
        sections.value.push({ id: ++index, section_name: "", section_type: sectionType, content: []})
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
        emit("updateSections", updatedSections)
    }

    // Whenever the sections information updates, emit to parent component
    watch(sections.value, (updatedSections) => {
        emit("updateSections", updatedSections)
    })

    // Whenever the sections are set by JSON, update sections accordingly
    watch(() => props.setSections, (newSetSections) => {
        // Remove previous section content
        while (sections.value.length > 0) {
            sections.value.pop()
        }

        // Remove previous set section content
        while (setSections.value.length > 0) {
            setSections.value.pop()
        }

        // Set list of sections based on JSON info
        // Determine what the max id is
        var idList: number[] = []
        for (let i = 0; i < newSetSections.length; i++) {
            idList.push(newSetSections[i].id)
            // Push sections based on order of id's to
            // set sections (which goes on to Section.vue)
            // and sections for this component
            // which preserves section info order upon import
            var section = { 
                id: newSetSections[i].id,
                section_name: newSetSections[i].section_name,
                section_type: newSetSections[i].section_type,
                content: newSetSections[i].content
            }
            sections.value.push(section)
            setSections.value.push(section)
        }
        // Set index to match the indices already used
        index = Math.max(...idList)
    })

</script>

<template>
    <div class="resume-sections">
        <h4 id="sections-title">Sections</h4>

        <!-- List of sections -->
        <div v-if="sections.length > 0" class="sections-list">
            <draggable :list="sections" item-key="id">
                <template #item="{element}">
                    <Section :id="element.id" :section-type="element.section_type" 
                        :set-sections="setSections"
                        @delete-section="(idToRemove) => removeSection(idToRemove)"
                        @update-title="(title) => (element.section_name = title)"
                        @update-section-experiences="(experiences) => (element.content = experiences)"
                        @update-lists="(lists: List[]) => (element.content = lists)"></Section>
                </template>
            </draggable>
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
        border-radius: 10px;
    }

    .section-list-buttons {
        display: flex;
    }

    button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }
</style>
