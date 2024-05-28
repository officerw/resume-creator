<script setup lang="ts">
    import { ref } from "vue"


    // Store information about this experience
    const experience = ref({
        title: "",
        location: "",
        organization: "",
        tenure: ""
    })

    let index = 0
    const details = ref([
        { id: ++index, info: "" }
    ])

</script>

<template>
    <div class="experience-container">
        <h5>Experience Description</h5>
        <textarea id="experience-title" v-model="experience.title" rows="1" name="experienceTitle" placeholder="Experience Title" maxlength="30"></textarea>
        <textarea id="experience-location" v-model="experience.location" rows="1" name="experienceLocation" placeholder="Experience Location" maxlength="30"></textarea>
        <textarea id="experience-organization" v-model="experience.organization" rows="1" name="experienceOrganization" placeholder="Experience Organization" maxlength="30"></textarea>
        <textarea id="experience-tenure" v-model="experience.tenure" rows="1" name="experienceTenure" placeholder="Experience Tenure" maxlength="30"></textarea>

        <h5>Experience Details</h5>
        <ul class="experience-details">
            <li v-for="detail in details">
                <textarea id="experience-detail" v-model="detail.info" rows="1" name="experienceDetail" placeholder="Experience Detail" maxlength="60"></textarea>
            </li>
        </ul>

        <div class="details-list-buttons">
            <button id="add-button" v-if="index<6" @click="addContactInfo()"><img class="contact-info-button-img" src="/static/plus.png" alt="+"/></button>
            <button id="remove-button" v-if="index>1" @click="removeContactInfo()"><img class="contact-info-button-img" src="/static/minus.png" alt="-"/></button>
        </div>
    </div>
</template>

<style>
    .experience-details ul.bullet {
        padding: 0;
    }
</style>
