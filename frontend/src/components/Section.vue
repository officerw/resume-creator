
<script setup lang="ts">
    import { onMounted, onUpdated, ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Experience from "./Experience.vue"
    import List from "./List.vue"

    type Experience = {
        id: number
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
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

    const emit = defineEmits(["deleteSection", "moveSectionUp", "moveSectionDown"])

    const numExperiences = ref(1) // Experience sections always have at least one experience
    const sectionInfo = defineModel<Section>("sectionInfo", {
        required: true
    })

    const numSections = defineModel("numSections", {
        type: Number,
        required: true
    })

    // Tell parent component to delete this section
    function deleteSection(idToRemove: number) {
        emit("deleteSection", idToRemove)
    }

    function addExperience() {
        numExperiences.value = numExperiences.value + 1

        // Get experience index
        let index = sectionInfo.value.exp_content.length + 1
        
        sectionInfo.value.exp_content.push({id: index, experience_title: "", location: "", organization: "", tenure: "", content: [""]})
    }

    function addList() {
        // Get list index
        let index = sectionInfo.value.list_content.length + 1
        
        sectionInfo.value.list_content.push({id: index, list_title: "", list_content: ""})
    }

    function removeExperienceOrList(removeList: boolean) {
        if (removeList) {
            sectionInfo.value.list_content.pop()
        } else {
            numExperiences.value = numExperiences.value - 1
            sectionInfo.value.exp_content.pop()
        }
    }

    function moveSectionUp(id: number) {
        emit("moveSectionUp", id)
    }

    function moveSectionDown(id: number) {
        emit("moveSectionDown", id)
    }

    // Move experience up in list of exp's
    function moveExpUp(idToMove: number) {
        var expToMoveUp = sectionInfo.value.exp_content[idToMove - 1]
        var expToMoveDown = sectionInfo.value.exp_content[idToMove - 2]

        // Set new id's for experiences
        expToMoveUp.id = expToMoveUp.id - 1
        expToMoveDown.id = expToMoveDown.id + 1

        // Swap experiences in list
        sectionInfo.value.exp_content[idToMove - 2] = expToMoveUp
        sectionInfo.value.exp_content[idToMove - 1] = expToMoveDown
    }

    // Move experience down in list of exp's
    function moveExpDown(idToMove: number) {
        var expToMoveUp = sectionInfo.value.exp_content[idToMove]
        var expToMoveDown = sectionInfo.value.exp_content[idToMove - 1]

        // Set new id's for experiences
        expToMoveUp.id = expToMoveUp.id - 1
        expToMoveDown.id = expToMoveDown.id + 1

        // Swap experiences in list
        sectionInfo.value.exp_content[idToMove - 1] = expToMoveUp
        sectionInfo.value.exp_content[idToMove] = expToMoveDown
    }

</script>

<template>
    <div class="resume-section-instance">
        <!-- Allow users to delete this selection and give some UI indication that the section is draggable -->
        <div id="section-header">
            <div id="section-move-ui">
                <button v-if="sectionInfo.id > 1" id="move-section-up" @click="moveSectionUp(sectionInfo.id)"><img src="/static/uparrow.png" alt="Move Section Up"></button>
                <button v-if="sectionInfo.id < numSections" id="move-section-down" @click="moveSectionDown(sectionInfo.id)"><img src="/static/downarrow.png" alt="Move Section Down"></button>
            </div>
            
            <button id="delete-section" @click="deleteSection(sectionInfo.id)"><img src="/static/close.png" alt="close"></button>
        </div>
        
        <!-- Allow the user to dictate the title of the section -->
        <div class="section-title">
            <h4 id="section-title-label">Section Title:</h4>
            <textarea id="section-title" v-model="sectionInfo.section_name" rows="1" name="sectionTitle" placeholder="Section Title Goes Here" maxlength="30"></textarea>
        </div>
        
        <!-- Here, we outline the layout of a list type section -->
        <div v-if="sectionInfo.section_type == 'list'" class="list-section">
            <div v-for="(list, i) in sectionInfo.list_content">
                <List v-model="sectionInfo.list_content[i]" />
            </div>

            <!-- Buttons to add/remove lists to this section -->
            <div class="lists-buttons">
                <button v-if="sectionInfo.list_content.length < 15" id="add-list" @click="addList()">Add List</button>
                <button v-if="sectionInfo.list_content.length > 1" id="remove-list" @click="removeExperienceOrList(true)">Remove List</button>
            </div>
        </div> <!-- Here, we outline the layout of a list of experiences type section and update experience details based on user input -->
        <div v-else class="experience-section">
            <div v-for="(experience, i) in sectionInfo.exp_content">
                <Experience v-model:experience-info="sectionInfo.exp_content[i]" 
                v-model:num-experiences="numExperiences"
                @move-exp-up="(idToMove) => moveExpUp(idToMove)"
                @move-exp-down="(idToMove) => moveExpDown(idToMove)"></Experience>
            </div>

            <!-- Buttons to add/remove experiences to this section -->
            <div class="experiences-buttons">
                <button v-if="sectionInfo.exp_content.length < 42" id="add-experience" @click="addExperience()">Add Experience</button>
                <button v-if="sectionInfo.exp_content.length > 1" id="remove-experience" @click="removeExperienceOrList(false)">Remove Experience</button>
            </div>
        </div>
    </div>
</template>

<style>
    #section-move-ui {
        display: inline-flex;
        width: 60%;
        margin: 5px;
        margin-left: 20%;
    }

    #move-section-up {
        margin: 0 5px;
    }

    #move-section-down {
        margin: 0 5px;
    }

    .resume-section-instance {
        background-color: white;
        border-radius: 7px;
        padding: 3px;
        margin: 8px 0;
    }


    .section-title {
        display: flex;
        padding: 0 0.5rem;
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
        margin: 5px;
    }

    .experiences-buttons, .lists-buttons {
        display: flex;
        padding: 0.25rem 0.5rem;
    }

    button.experiences-buttons button.lists-buttons {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }


    
</style>
