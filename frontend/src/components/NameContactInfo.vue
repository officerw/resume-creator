<script setup lang="ts">
    import { ref } from "vue"

    // Give each contact information field an index
    let index = 0

    const name = ref("")
    const contacts = ref([
        { id: ++index, info: "" }
    ])


    // Add another field of contact information
    function addContactInfo() {
        contacts.value.push(
            { id: ++index, info: "" }
        )
        console.log(contacts.value[contacts.value.length - 1].id)
    }

    // Remove field of contact information
    function removeContactInfo() {
        contacts.value.pop()
        index -= 1
    }

    // Print out contact info
    function print() {
        for (let i = 0; i < contacts.value.length; i++) {
            console.log(contacts.value[i])
        }
    }

</script>

<template>
    <div class="name-contact-info-container">
        <h4>Name/Title of Resume:</h4>
        <textarea id="name" v-model="name" rows="1" name="Name" placeholder="Name/Title Goes Here" maxlength="50"></textarea>
        <h4>Contact Information:</h4>
        <ul>
            <li v-for="contact in contacts" :key="contact.id">
                <textarea v-model="contact.info" rows="1" name="ContactInfo" v-bind:placeholder="'Contact Information ' + contact.id.toString()" maxlength="50"></textarea>
            </li>
        </ul>

        <div class="contact-list-buttons">
            <button id="add-button" v-if="index<6" @click="addContactInfo()">+</button>
            <button id="remove-button" v-if="index>1" @click="removeContactInfo()">-</button>
        </div>

        <button @onclick="print()">plos</button>
    </div>
</template>

<style>
    .name-contact-info-container {
        width: 100%;
        height: 100%;
    }

    .contact-list-buttons {
        display: flex;
    }

    textarea {
        padding: 5px;
        border-radius: 5px;
        width: 100%;
        resize:none;
    }

    ul {
        list-style: none;
        padding: 0;
    }

    #name {
        resize:none;
        overflow-x: hidden;
    }

    button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }

    #add-button {
        background-color: lightgreen;
    }

    #remove-button {
        background-color: lightcoral
    }

</style>
