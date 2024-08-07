<!--
  APP

  This page consists of the visual information that will always remain on the app,
  including a header, navbar, and footer.
-->

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <!--
	  Header of the webpage is always present, regardless of the router view selected
	  This way, the title and navbar are always present for the user to see and use
  -->
  <header>
    <div class="title">
      <h1>Resume Creator</h1>
    </div>

    <div class="navbar">
      <nav>
        <ul>
          <li class="navbar-item"><RouterLink to="/">Resume Editor</RouterLink></li>
        </ul>
      </nav>
    </div>
  </header>

  <RouterView />

  <!--
	  Footer is always present, containing information on the authorship of this webpage.
  -->
  <footer>
    <p class="footer">
      This website was created by William Officer, using Vue JS, Flask, and pdflatex. To reference the source code for this project, visit its <a href="https://github.com/officerw/resume-creator">GitHub repository</a>. 2024 © Copyright William Officer.
    </p>
  </footer>
</template>

<style scoped>
  header {
    height: var(--header-height);
    width: 100%;
    padding: 0 10% 0 10%;
    align-items: center;
    display: flex;
    background-color: #0461cf;
    justify-content: space-evenly;
  }

  .navbar-item a {
    font-size: calc(5px + var(--normal-font-size));
  }

  header h1 {
    color: white;
    padding: 0 2rem 0 2rem;
    vertical-align: middle;
    font-size: var(--title-font-size);
  }

  nav {
    height: 100%;
    width: 100%;
  }

  .navbar {
    height: var(--header-height);
    display:flex;
    align-items: center;
    justify-content: center;
    width: max-content;
  }

  .navbar ul {
    list-style-type: none;
    height: 100%;
    width: 100%;
    padding: 0;
    display: flex;
  }

  ul > li {
    display: inline-block;
    height: 100%;
    margin: 0 2rem;
  }

  .navbar-item li {
    padding: 0 2rem;
  }

  li a {
    text-decoration: none;
    color: #00bf7d;
    font-size: large;
    height: 100%;
    padding: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  li a:hover {
    background-color: rgba(0, 191, 125, 0.25);
  }

  footer {
    width: 100%;
    bottom:0;
    padding: 0 10% 0 10%;
    height: 3rem;
    background-color: #054fb9;
    color: white;
    text-align: center;
    display: flex;
    font-size: var(--normal-font-size);
    justify-content: center;
    align-items: center;
  }

  footer a {
    color: #00bf7d;
    text-decoration: none;
  }

  footer a:hover {
    background-color: rgba(0, 191, 125, 0.25);
  }
</style>
