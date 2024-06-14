
<script setup lang="ts">
    import { onMounted, onUpdated, ref, watch } from "vue"
    import draggable from "vuedraggable"
    import Experience from "./Experience.vue"
    import List from "./List.vue"

    const sectionTitle = ref("")

    // Delete this section when requested
    const emit = defineEmits(["deleteSection", "updateTitle", "updateSectionExperiences", "updateLists"])

    // Accept whether this section is a list type or experience type
    // Accept info set by JSON
    const props = defineProps({
        sectionType: {
            type: String,
            required: true
        },
        id: {
            type: Number,
            required: true
        },
        setSections: {
            type: Array<Section>,
            required: true
        }
    })

    // Store a list of experiences
    let indexExp = 0
    const experiences = ref([
        { id: ++indexExp, experience_title: "", location: "", organization: "", tenure: "", content: [""]}
    ])

    // Store list of lists
    let indexList = 0
    const lists = ref([
        { id: ++indexList, list_title: "", list_content: ""}
    ])

    // If the user imports info via JSON, we set the lists
    // using the setContent list of content
    var setContentVal: (Experience | List)[] = []
    const setContent = ref(setContentVal)

    // Tell parent component to delete this section
    function deleteSection(idToRemove: number) {
        emit("deleteSection", idToRemove)
    }

    function addExperience() {
        experiences.value.push({
            id: ++indexExp, experience_title: "", location: "", organization: "", tenure: "", content: [""]
        })
    }

    function removeExperience() {
        experiences.value.pop()
        indexExp -= 1
    }

    function addList() {
        lists.value.push({ id: ++indexList, list_title: "", list_content: ""})
    }

    function removeList() {
        lists.value.pop()
        indexList -= 1
    }

    type Experience = {
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    type List = {
        list_title: string
        list_content: string
    }

    type Section = {
        id: number
        section_name: string
        section_type: string
        content: Array<List | Experience>
    }

    // If the section info has been set by JSON upon mount, set the values for
    // this
    onMounted(() => {
        if (props.setSections.length > 0) {
            updateWithJSON(props.setSections)
        }
    })

    // Whenever the section info set by JSON changes, set the values for this
    // component accordingly
    watch(() => props.setSections, (newSetSections) => {
        updateWithJSON(newSetSections)
    })

    // Update based on JSON info
    function updateWithJSON(newSetSections: Section[]) {
        var newSetSection = newSetSections.find((element) => element.id == props.id)

        if (newSetSection == undefined) {
            return
        }

        sectionTitle.value = newSetSection.section_name
        // setContent is a prop going to the actual content Components
        // in this section
        setContent.value = newSetSection.content

        // Remove all existing lists
        while (lists.value.length > 1) {
            removeList()
        }
        
        // Remove all existing experiences
        while (experiences.value.length > 1) {
            removeExperience()
        }
        
        // Add all necessary lists/experiences beyond the first
        // list/experience
        for (let i = 1; i < setContent.value.length; i++) {
            if (props.sectionType == "list") {
                addList()
            } else {
                addExperience()
            }
        }
    }

    // Whenever the title changes, emit the value to the parent component
    watch(sectionTitle, (newTitle) => {
        emit("updateTitle", newTitle)
    })

    // Whenever experience information changes provided by the user, emit the value to parent component
    watch(experiences.value, (newExperiences) => {
        emit("updateSectionExperiences", newExperiences)
    })

    // Whenever the lists change, emit the value to the parent component
    watch(lists.value, (newLists) => {
        var lists: List[] = []
        for (let i = 0; i < newLists.length; i++) {
            lists.push({ list_title: newLists[i].list_title, list_content: newLists[i].list_content })
        }

        emit("updateLists", lists)
    })

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
            <div v-for="list in lists">
                <List :id="list.id"
                :content="setContent" 
                @update-list-title="(newTitle) => (list.list_title = newTitle)" 
                @update-list-content="(newContent) => (list.list_content = newContent)" />
            </div>

            <!-- Buttons to add/remove lists to this section -->
            <div class="lists-buttons">
                <button v-if="lists.length < 15" id="add-list" @click="addList()">Add List</button>
                <button v-if="lists.length > 1" id="remove-list" @click="removeList()">Remove List</button>
            </div>
        </div> <!-- Here, we outline the layout of a list of experiences type section and update experience details based on user input -->
        <div v-else class="experience-section">
            <draggable :list="experiences" item-key="id">
                <template #item="{element}">
                    <Experience :id="element.id"
                    :content="setContent"
                    @update-experience="(experience: Experience) => {
                        element.experience_title = experience.experience_title
                        element.location = experience.location
                        element.organization = experience.organization
                        element.tenure = experience.tenure
                    }"
                    @update-experience-details="(details: string[]) => {
                        element.content = details
                    }" />
                </template>
            </draggable>

            <!-- Buttons to add/remove experiences to this section -->
            <div class="experiences-buttons">
                <button v-if="experiences.length < 42" id="add-experience" @click="addExperience()">Add Experience</button>
                <button v-if="experiences.length > 1" id="remove-experience" @click="removeExperience()">Remove Experience</button>
            </div>
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
        margin: 5px;
    }

    .experiences-buttons {
        display: flex;
    }

    .experiences-buttons button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }

    
</style>
