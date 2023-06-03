<template>
    <div class="home">
        <h1>ImageVideoUpscaler</h1>

        <label for="algorithm">Upscaler engine</label><br>
        <select name="engine" id="engine" v-model="upscaleSettings.engine">
            <option v-for="engine in engines" :key="engine.id" :value="engine.id">{{ engine.displayName }}</option>
        </select><br>

        <label for="algorithm">Upscaling algorithm</label><br>
        <select name="algorithm" id="algorithm" v-model="upscaleSettings.algorithm">
            <option v-for="engine in engines[ upscaleSettings.engine ][ 'modes' ]" :key="engine.id" :value="engine.id">{{ engine.displayName }}</option>
        </select><br>

        <label for="scale" v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'upscaling' )">Scale factor</label><br>
        <input type="number" name="scale" id="scale" v-model="upscaleSettings.scale" min="2" max="4" onkeydown="return false">x<br>

        <label for="sharpening" v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'sharpening' )">Sharpening factor</label><br>
        <input type="number" step="0.01" name="scale" id="scale" v-model="upscaleSettings.sharpening" min="0" max="1"><br>

        <button @click="runCommand( 'InputFile' )">Input file</button><br>
        <button @click="runCommand( 'OutputFile' )">Output file</button><br>
        <button @click="start()">Start upscaling</button>
    </div>
</template>

<script>
export default {
    name: 'HomeView',
    data() {
        return {
            upscaleSettings: { 'engine': 'ffc', 'algorithm': 'fsr', 'scale': 2, 'sharpening': 0, 'InputFile': '', 'OutputFile': '' },
            engines: { 'ffc':{ 'displayName': 'FidelityFX CLI', 'id': 'ffc', 'modes': { 'fsr': { 'displayName': 'FidelityFX Super Resolution', 'id': 'fsr' } }, 'supports': [ 'upscaling', 'sharpening' ] }, 'ss':{ 'displayName': 'REAL-ESGRAN', 'id': 'ss' } },
        }
    },
    methods: {
        runCommand ( command ) {
            fetch( 'http://127.0.0.1:8081/api/get' + command ).then( res => {
                res.json().then( data => {
                    this.upscaleSettings[ command ] = data[ 'data' ];
                } ).catch( error => {
                    console.log( error );
                } );
            } );
        },
        start() {
            let fetchOptions = {
                method: 'post',
                body: JSON.stringify( this.upscaleSettings ),
                headers: {
                    'Content-Type': 'application/json',
                    'charset': 'utf-8'
                },
            }
            fetch( 'http://127.0.0.1:8081/api/startUpscaling', fetchOptions ).then( res => {
                res.json().then( data => {
                    console.log( data );
                } ).catch( error => {
                    console.log( error );
                } )
            } );
        }
    }
}
</script>
