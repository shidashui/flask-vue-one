<template>
    <div class="container">
      <alert
        v-for="(alert,index) in alerts" :key="index"
        v-if="alert.showAlert"
        v-bind:variant="alert.variant"
        v-bind:message="alert.message">
      </alert>
      <button type="button" class="btn btn-primary">HomePage</button>
    </div>
</template>

<script>
    import Alert from "./Alert";
    export default {
        name: "Home",
      components: {
          alert:Alert
      },
      data(){
          return{
            alerts:[
              {
                showAlert: true,
                variant: 'info',
                message: 'Hi'
              },
              {
                showAlert:true,
                variant: 'danger',
                message: 'Oops..'
              },
              {
                showAlert:true,
                variant: 'success',
                message: 'OK'
              }
            ]
          }
      }
    }
</script>

<style scoped>

</style>
