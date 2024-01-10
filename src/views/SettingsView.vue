<template>
    <div class="about">
        <h1>Settings</h1>
        <p>WIP!</p>
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
            fetch( 'http://127.0.0.1:49369/api/getEngines' ).then( res => {
                console.log( res );
                res.json().then( data => {
                    this.engines = data.body;
                } );
            } ).catch( error => {
                console.log( error );
            } );
        }
    },
    created() {
    }
}
</script>
