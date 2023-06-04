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

        <div v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'upscaling' )">
            <label for="scale">Scale factor</label><br>
            <input type="number" name="scale" id="scale" v-model="upscaleSettings.scale" min="2" max="4" onkeydown="return false">x<br>
        </div>

        <div v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'sharpening' )">
            <label for="sharpening">Sharpening factor</label><br>
            <input type="number" step="0.01" name="scale" id="scale" v-model="upscaleSettings.sharpening" min="0" max="1"><br>
        </div>

        <button @click="runCommand( 'InputFile' )">Input file</button><br>
        <button @click="runCommand( 'OutputFile' )">Output file</button><br>
        <button @click="start()">Start upscaling</button>

        <div class="output-box-wrapper">
            <p id="cmd" @click="showCmdOutput()">Command output</p>
            <div class="output-box" v-html="output" id="output">
            </div>
        </div>

        <dialog id="processing">
            <div class="dialog-container">
                Your file is being processed. You will be notified when the upscaling process has finished.
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="wrong">
            <div class="dialog-container">
                Some entries are missing. Please ensure that you have specified an input and output file!
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="fileExtension">
            <div class="dialog-container">
                File extension of input and output file don't match! Please ensure that they are the same.
                Click the button below to fix it.
                <button @click="fixFileExtension();">Fix</button>
                <p v-if="fixed">Fixed!</p>
                <form method="dialog">
                    <button @click="this.fixed = false;">OK</button>
                </form>
            </div>
        </dialog>
    </div>
</template>

<script>
import { socket } from "@/socket";

export default {
    name: 'HomeView',
    data() {
        return {
            upscaleSettings: { 'engine': 'ffc', 'algorithm': 'fsr', 'scale': 2, 'sharpening': 0, 'InputFile': [ '/home/janis/projects/myevent/assets/logo.png' ], 'OutputFile': '/home/janis/Downloads/test.png' },
            engines: { 'ffc':{ 'displayName': 'FidelityFX CLI', 'id': 'ffc', 'modes': { 'fsr': { 'displayName': 'FidelityFX Super Resolution', 'id': 'fsr' }, 'c': { 'displayName': 'Cubic', 'id': 'c' }, 'hqc': { 'displayName': 'High Quality Cubic', 'id': 'hqc' } }, 'supports': [ 'upscaling', 'sharpening' ] }, 'ss':{ 'displayName': 'REAL-ESRGAN', 'id': 'ss', 'modes': { 'av3': { 'displayName': 'realesr-animevideov3', 'id': 'av3' }, 'x4plus': { 'displayName': 'realesrgan-x4plus-anime', 'id': 'x4plus' } }, 'supports': [ 'upscaling' ] } },
            fixed: false,
            output: '',
        }
    },
    methods: {
        runCommand ( command ) {
            fetch( 'http://127.0.0.1:49369/api/get' + command ).then( res => {
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
            fetch( 'http://127.0.0.1:49369/api/startUpscaling', fetchOptions ).then( res => {
                res.json().then( data => {
                    console.log( this.upscaleSettings );
                    if ( data.data == 'upscaling' ) {
                        document.getElementById( 'processing' ).showModal();
                    } else if ( data.data == 'dataMissing' ) {
                        document.getElementById( 'wrong' ).showModal();
                    } else {
                        document.getElementById( 'fileExtension' ).showModal();
                    }
                } ).catch( error => {
                    console.log( error );
                } )
            } );
            this.output = '';

            socket.on( 'progress', ( ...args) => {
                this.output += args + '<br>';
            } )
        },
        showCmdOutput () {
            document.getElementById( 'output' ).classList.toggle( 'shown' );
        },
        fixFileExtension () {
            let fileExtension = this.upscaleSettings.InputFile[ 0 ].substring( this.upscaleSettings.InputFile[ 0 ].length - 4 );
            this.upscaleSettings.OutputFile = this.upscaleSettings.OutputFile.slice( 0, this.upscaleSettings.OutputFile[ 0 ].length - 5 ) + fileExtension;
            this.fixed = true;
        }
    },
    created() {
        socket.connect();
    },
    deactivated() {
        socket.disconnect();
    }
}
</script>

<style scoped>
    .output-box-wrapper {
        margin-top: 5%;
        width: 100%;
        height: 20%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .output-box {
        display: none;
        overflow: scroll;
        height: 100%;
        width: 60%;
        text-align: justify;
    }

    .shown {
        display: block;
    }

    dialog {
        border-radius: 10px;
        height: 30vh;
        width: 30vw;
        background-color: var( --background-color );
        border-style: none;
        color: var( --primary-color );
    }

    .dialog-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    #cmd {
        text-align: justify;
        width: 60%;
        cursor: pointer;
        user-select: none;
    }
</style>
