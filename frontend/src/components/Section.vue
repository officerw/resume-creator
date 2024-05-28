
<script setup lang="ts">
    import { ref } from "vue"
    import draggable from "vuedraggable"
    import Experience from "./Experience.vue"

    const sectionTitle = ref("")

    // Delete this section when requested
    const emit = defineEmits(["deleteSection"])

    // Accept whether this section is a list type or experience type
    const props = defineProps({
        sectionType: {
            type: String,
            required: true
        },
        id: {
            type: Number,
            required: true
        }
    })

    const experiences = ref([
        { id: 1, title: "", location: "", organization: "", tenure: "", content: []}
    ])

    // Tell parent component to delete this section
    function deleteSection(idToRemove: number) {
        emit("deleteSection", idToRemove)
    }

</script>

<template>
    <div class="resume-section-instance">
        <!-- Allow users to delete this selection and give some UI indication that the section is draggable -->
        <div id="section-header">
            <img id="draggable-ui" src="/static/drag.png" alt="draggable">
            <button id="delete-section" @click="deleteSection(id)"><img src="/static/close.png" alt="close"></button>
        </div>
        
        <!-- Allow the user to dictate the title of the section -->
        <div class="section-title">
            <h4 id="section-title-label">Section Title:</h4>
            <textarea id="section-title" v-model="sectionTitle" rows="1" name="sectionTitle" placeholder="Section Title Goes Here" maxlength="30"></textarea>
        </div>
        

        <!-- Here, we outline the layout of a list type section -->
        <div v-if="sectionType == 'list'" class="list-section">
            I am a list
        </div> <!-- Here, we outline the layout of a list of experiences type section -->
        <div v-else class="experience-section">
            <draggable v-model="experiences" item-key="id">
                <template #item="{element}">
                    <Experience/>
                </template>
            </draggable>
        </div>
    </div>
</template>

<style>
    .resume-section-instance {
        background-color: white;
        border-radius: 7px;
        padding: 3px;
        margin: 3px 0;
    }


    .section-title {
        display: flex;
    }

    #section-title-label {
        padding-right: 5px;
    }

    #draggable-ui {
        position: relative;
        left: calc(50% - 0.5rem);
    }

    #draggable-ui:hover {
        cursor: grab;
    }

    #section-header {
        width: 100%;
        display: inline-block;
        position: relative;
    }

    #section-title {
        display: flex;
        flex-direction:row;
        flex: 1;
    }

    #delete-section {
        background-color: lightcoral;
        float: right;
    }
    
</style>
