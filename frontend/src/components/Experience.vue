<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"

    type Experience = {
        id: number
        experience_title: string
        location: string
        organization: string
        tenure: string
        content: string[]
    }

    const experienceInfo = defineModel<Experience>({
        default: {
            id: 1,
            experience_title: "",
            location: "",
            organization: "",
            tenure: "",
            content: [""]
        },
        required: true
    })

    // Add experience detail
    function addDetail() {
        experienceInfo.value.content.push("")
    }

    // Remove experience detail
    function removeDetail() {
        experienceInfo.value.content.pop()
    }

    //const experienceDetailEntries = document.getElementsByClassName("experience-detail-textarea")
    //            for (let i = 0; i < experienceDetailEntries.length; i++) {
    //                var currExperienceDetailEntry = experienceDetailEntries[i]
    //                var scrollHeight = currExperienceDetailEntry.scrollHeight
    //                currExperienceDetailEntry.setAttribute("style", "height:" + scrollHeight + "px")
    //            }

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
            <textarea id="experience-title" v-model="experienceInfo.experience_title" rows="1" name="experienceTitle" placeholder="Experience Title" maxlength="100"></textarea>
            <textarea id="experience-location" v-model="experienceInfo.location" rows="1" name="experienceLocation" placeholder="Experience Location" maxlength="100"></textarea>
            <textarea id="experience-organization" v-model="experienceInfo.organization" rows="1" name="experienceOrganization" placeholder="Experience Organization" maxlength="100"></textarea>
            <textarea id="experience-tenure" v-model="experienceInfo.tenure" rows="1" name="experienceTenure" placeholder="Experience Tenure" maxlength="100"></textarea>

            <!-- Textareas where the user can enter details of the experience -->
            <h5>Experience Details</h5>
            <ul class="experience-details">
                <li class="experience-detail" style="display:flex;padding:5px 0;" v-for="(detail, i) in experienceInfo.content">
                    <img style="height:30px;padding:10px 5px;" src="/static/bullet.png">
                    <textarea oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"' class="experience-detail-textarea" v-model="experienceInfo.content[i]" rows="1" name="experienceDetail" placeholder="Experience Detail" maxlength="800"></textarea>
                </li>
            </ul>

            <!-- Buttons that allow the user to add or remove details of the experience -->
            <div class="details-list-buttons">
                <button id="add-button-detail" v-if="experienceInfo.content.length < 5" @click="addDetail()">Add Experience Detail</button>
                <button id="remove-button-detail" v-if="experienceInfo.content.length > 1" @click="removeDetail()">Remove Experience Detail</button>
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

    .expereince-details {
        padding: 0;
        margin: 0;
        margin-left: 1rem;
    }

    .expereince-detail {
        display: flex;
    }

    ul.experience-details {
        list-style-type: none;
        padding: 0;
    }

    .expereince-detail {
        background-image: url("/static/bullet.png");
        background-repeat: no-repeat;
        background-position: 0 0.4rem;
        padding-left: 0.6rem;
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
