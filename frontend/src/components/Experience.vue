<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"

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

    // Emit experience context and details to parent component
    const emit = defineEmits(["updateExperience", "updateExperienceDetails"])
    // Props to accept imported JSON info
    const props = defineProps({
        content: {
            type: Array<Experience | List>,
            required: true
        },
        id: {
            type: Number,
            required: true
        }
    })

    // Store information about this experience
    const experience = ref({
        experience_title: "",
        location: "",
        organization: "",
        tenure: ""
    })

    // Store list of details related to the experience
    let index = 0
    const details = ref([
        { id: ++index, info: "" }
    ])

    // Add experience detail
    function addDetail() {
        details.value.push({
            id: ++index, info: ""
        })
    }

    // Remove experience detail
    function removeDetail() {
        details.value.pop()
        index -= 1
    }

    // Whenever experience information updates, emit to parent component
    watch(experience.value, (newExperience) => {
        emit("updateExperience", newExperience)
    })

    // Whenever experience details update, emit to parent component
    watch(details.value, (newDetails) => {
        // Convert details from object to list of strings
        var newDetailsList = []
        for (let i = 0; i < newDetails.length; i++) {
            newDetailsList.push(newDetails[i].info)
        }

        emit("updateExperienceDetails", newDetailsList)
    })

    // Whenever the content value set by JSON changes, update
    // textarea content
    watch(() => props.content, (newContent) => {
        if (newContent != undefined)
            updateExpWithJSON(newContent)
    })

    // If the experience info has been set by JSON upon mount, set textarea
    // values accordingly
    onMounted(() => {
        if (props.content != undefined)
            updateExpWithJSON(props.content)
    })

    // Update textareas upon JSON import
    function updateExpWithJSON(newContent: (Experience | List)[]) {
        // Remember that newContent is just the list of all imported content
        // for the section this experience is inside
        if (newContent != undefined && props.id <= newContent.length) {
            var newExp = newContent[props.id - 1]
            // Type guard newExp is in fact a Experience, not a List
            if ("experience_title" in newExp) {
                experience.value.experience_title = newExp.experience_title
                experience.value.location = newExp.location
                experience.value.organization = newExp.organization
                experience.value.tenure = newExp.tenure

                // Remove previously existing details
                while (details.value.length > 1) {
                    removeDetail()
                }

                // Add all necessary details beyond first
                for (let i = 1; i < newExp.content.length; i++) {
                    addDetail()
                }

                // Add details info from JSON
                details.value[0].info = newExp.content[0]
                for (let i = 1; i < newExp.content.length; i++) {
                    details.value[i].info = newExp.content[i]
                }
            }
        }
    }

</script>

<template>
    <div class="experience-container">
        <!-- img to indicate that experiences are draggable -->
        <div class="experience-draggable-ui">
            <img src="/static/drag.png" alt="draggable">
        </div>

        <div class="experience-info">
                <!-- Textareas where users can enter the context of the experience -->
            <h5>Experience Description</h5>
            <textarea id="experience-title" v-model="experience.experience_title" rows="1" name="experienceTitle" placeholder="Experience Title" maxlength="30"></textarea>
            <textarea id="experience-location" v-model="experience.location" rows="1" name="experienceLocation" placeholder="Experience Location" maxlength="30"></textarea>
            <textarea id="experience-organization" v-model="experience.organization" rows="1" name="experienceOrganization" placeholder="Experience Organization" maxlength="30"></textarea>
            <textarea id="experience-tenure" v-model="experience.tenure" rows="1" name="experienceTenure" placeholder="Experience Tenure" maxlength="30"></textarea>

            <!-- Textareas where the user can enter details of the experience -->
            <h5>Experience Details</h5>
            <ul class="experience-details">
                <li v-for="detail in details">
                    <textarea id="experience-detail" v-model="detail.info" rows="1" name="experienceDetail" placeholder="Experience Detail" maxlength="60"></textarea>
                </li>
            </ul>

            <!-- Buttons that allow the user to add or remove details of the experience -->
            <div class="details-list-buttons">
                <button id="add-button-detail" v-if="index<5" @click="addDetail()">Add Experience Detail</button>
                <button id="remove-button-detail" v-if="index>1" @click="removeDetail()">Remove Experience Detail</button>
            </div>
        </div>
    </div>
</template>

<style>
    .experience-draggable-ui {
        display: flex;
        width: 100%;
        justify-content: center;
    }

    .experience-draggable-ui img:hover {
        cursor: grab;
    }

    .experience-container {
        border-style: dotted;
        display: inline-block;
        padding: 8px;
        margin: 0.5rem;
        width: calc(100% - 1rem);
    }

    .details-list-buttons {
        display: flex;
        padding: 0 2rem;
    }
    
    .details-list-buttons button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }
</style>
