
<script setup lang="ts">
    import { ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Section from "./Section.vue"
import type { RefSymbol } from "@vue/reactivity";

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

    type SectionInfo = {
        id: number
        name: string
        type: string
        content: (List|Experience)[]
    }

    // Define index and reactive list of section information
    var index = 0
    const val: SectionInfo[] = []
    const sections = ref(val)

    // Add a section based on the type
    function addSection(sectionType: string) {
        sections.value.push({ id: ++index, name: "", type: sectionType, content: []})
    }

    // Remove a section when the user deletes it
    function removeSection(idToRemove: Number) {
        // Remove section to be removed by filtering out its id
        sections.value = sections.value.filter((element) => element.id != idToRemove)
    }

    // debug
    watch(sections.value, (s) => {
        console.log(s)
    })

</script>

<template>
    <div class="resume-sections">
        <h4>Sections</h4>

        <!-- List of sections -->
        <div v-if="sections.length > 0" class="sections-list">
            <draggable v-model="sections" item-key="id">
                <template #item="{element}">
                    <Section :id="element.id" :section-type="element.type" 
                        @delete-section="(idToRemove) => removeSection(idToRemove)"
                        @update-title="(title) => (element.name = title)"
                        @update-section-experiences="(experiences) => (element.content = experiences)"></Section>
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
