
<script setup lang="ts">
    import { ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Section from "./Section.vue"

    type SectionInfo = {
        id: number
        type: string
    }

    // Define index and reactive list of section information
    var index = 0
    const sections = ref<SectionInfo[]>([])

    // Add a section based on the type
    function addSection(sectionType: string) {
        sections.value.push({ id: ++index, type: sectionType})
    }

    // Remove a section when the user deletes it
    function removeSection(idToRemove: Number) {
        // Remove section to be removed by filtering out its id
        sections.value = sections.value.filter((element) => element.id != idToRemove)
    }

</script>

<template>
    <div class="resume-sections">
        <h4>Sections</h4>

        <!-- List of sections -->
        <div v-if="sections.length > 0" class="sections-list">
            <draggable v-model="sections" item-key="id">
                <template #item="{element}">
                    <Section :id="element.id" :section-type="element.type" @delete-section="(idToRemove) => removeSection(idToRemove)"></Section>
                </template>
            </draggable>
        </div>

        <!-- The following section allows the user to add different kinds of sections to the resume builder -->
        <div class="contact-list-buttons">
            <button id="add-experience" @click="addSection('experience')">Add Experience Section</button>
            <button id="add-list" @click="addSection('list')">Add List Section</button>
        </div>
    </div>
</template>

<style>

</style>
