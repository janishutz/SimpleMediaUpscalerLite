<template>
    <div class="about">
        <h1>Settings</h1>
        <h3>Engines</h3>
        <p>{{ engines }}</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            engines: '',
        }
    },
    methods: {
        run() {
            fetch( 'http://127.0.0.1:8081/api/getEngines' ).then( res => {
                res.json().then( data => {
                    this.engines = data.body;
                } );
            } );
        }
    }
}
</script>
