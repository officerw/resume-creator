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

    const emit = defineEmits(["moveExpUp", "moveExpDown"])

    // The total number of experiences for the section the experience is contained in
    const numExperiences = defineModel("numExperiences", {
        type: Number,
        required: true
    })

    const experienceInfo = defineModel<Experience>("experienceInfo", {
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

    // Move this experience upwards in the list of experiences
    // for the section it is in
    function moveExpUp(idToMove: number) {
        emit("moveExpUp", idToMove)
    }

    // Move this experience downwards in the list of experiences
    // for the section it is in
    function moveExpDown(idToMove: number) {
        emit("moveExpDown", idToMove)
    }

</script>

<template>
    <div class="experience-container">
        <!-- img to indicate that experiences are draggable -->
        <div class="experience-move-ui">
            <button v-if="experienceInfo.id > 1" id="move-exp-up" @click="moveExpUp(experienceInfo.id)"><img src="/static/uparrow.png" alt="Move Experience Up"></button>
            <button v-if="experienceInfo.id < numExperiences" id="move-exp-down" @click="moveExpDown(experienceInfo.id)"><img src="/static/downarrow.png" alt="Move Experience Down"></button>
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
    .experience-move-ui {
        display: flex;
        width: 100%;
        justify-content: center;
        padding: 0 20%;
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
