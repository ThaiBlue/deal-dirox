<template>
  <div class="vue-app">
                                <!-- Event -->
        <!-- <h1>Events</h1> 
        <button @click.once="add(1)">Add</button>
        <button @click="subtract(1)">Subtract</button>
        <button @dblclick="add(10)">Add 10</button>
        <button @dblclick="subtract(10)">Subtract 10</button>
        <p>Number is: {{num}} </p>
        <a @click.prevent="click" href="http://www.google.com">Hello</a> -->
        <!-- <p> {{test()}} </p> -->


                                <!-- <h1>Keyboard Events</h1>
        <label>Name: </label>
        <input type="text" v-model="name"><br><br>
        <span>{{name}}</span>
        <label>Age: </label>
        <input type="text" v-model="age" placeholder="hello from the otherside">
        <span>{{age}}</span> -->


                                <!-- <h1>Computed Properties</h1> -->
        <!-- <button @click="a++">Add to A</button>
        <button @click="b++">Add to B</button>
        <p>A - {{a}}</p>
        <p>B - {{b}}</p>
        <p>Age + A = {{addtoA}} </p>
        <p>Age + B = {{addtoB}} </p> -->


        <!-- Dynamic CSS -->
        <h1>Dynamic CSS</h1>
        <!-- <h2>Example 1</h2>
        <div @click="available = !available" :class="{available: available}">
            <span>Faker</span>
        </div> -->
        <h2>Example 2</h2>
        <button @click="nearby = !nearby">Toggle Nearby</button>
        <button @click="available = !available">Toggle available</button>
        <div :class="compClass">
            <span>Faker</span>
        </div>


        <!-- <h1>Conditionals</h1>
        <button @click="error = !error">Toggle Error</button>
        <button @click="success = !success">Toggle Success</button> -->
        <!-- <p v-if="error">Error</p>
        <p v-else-if="success">Success Motherfucker</p> -->

        <!-- <p v-show="error">Error</p>
        <p v-show="Success"></p> -->


        <!-- <h1>Looping list</h1>
        <ul>
            <li v-for="char in characters" :key="char">{{ char }}</li>
        </ul>

        <ul>
            <li v-for="ninja in ninjas" :key="ninja">{{ninja.name}} - {{ninja.age}}</li>
        </ul>

        <li>{{ninjas[0].name}}</li>


        <template v-for="(ninja, index) in ninjas">
            <h3 :key="(ninja,index)">{{index}}.{{ninja.name}}</h3>
            <p :key=(index)>{{index}}.{{age}}</p>
        </template>


        <template v-for="ninja in ninjas">
            <div v-for="(val,key) in ninja" :key="(key, val)">
                <p> {{key}} - {{val}}</p>
            </div>
        </template>-->


        <!-- bag image -->
        <div class="bag">

        </div>

        
        <!-- bag health -->
        <div class="bag-health">
            <div></div>
        </div>


        <!-- game control -->
        <div class="control">
            <!-- <button>Punch</button>
            <button>Restart</button> -->
        </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            // name: '',
            // age: 20,
            // a: 0,
            // b: 6,
            available: false,
            // nearby: false,
            // error: false,
            // success: false
            characters: ['tien', 'someone', 'something'],
            ninjas: [
                {name: 'Ryu', age: 25},
                {name: 'Tien handsome', age: 21},
                {name: 'Another name', age: 32}
            ]
        }
    },

    methods: {
        // add(inc) {
        //     this.num += inc
        // },

        // subtract(dec){
        //     this.num -= dec
        // },

        // click() {
        //     alert('SUPRISE MOTHER FUCKER')
        // }

        // logName() {
        //     console.log('Name entered') 
        // },

        // logAge() {
        //     console.log('Age entered')
        // }

    },


    computed: {
        // addtoA() {
        //     console.log('A added')
        //     return this.a + this.age
        // },

        // addtoB() {
        //     console.log('B added')
        //     return this.b + this.age
        // }

        compClass() {
            return {
                available: this.available,
                nearby: this.nearby
            }
        }
    }
}
</script>

<style scoped>
    span {
        background: red;
        display: inline-block;
        padding: 10px;
        color: #fff;
        margin: 10px 0;
        cursor: pointer;
    }

    .available span {
        background: green;
    }

    .nearby span:after {
        content: "nearby";
        margin-left: 10px;
    }

    .bag {
        width: 200px;
        height: 500px;
        margin: 0 auto;
        /* background: url; */
    }
</style>